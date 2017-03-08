#include <config.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <status.h>
#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif
#ifdef _WIN32
 #include <winsock2.h>
#else
 #include <pwd.h>
 #define INVALID_SOCKET -1
#endif


#ifndef _WIN32
#endif

#include "mdsip_connections.h"

////////////////////////////////////////////////////////////////////////////////
//  Parse Host  ////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

static void ParseHost(char *hostin, char **protocol, char **host)
{
  size_t i;
  *protocol = strcpy((char *)malloc(strlen(hostin) + 10), "");
  *host = strcpy((char *)malloc(strlen(hostin) + 10), "");
  sscanf(hostin, "%[^:]://%s", *protocol, *host);
  if (strlen(*host) == 0) {
    if (hostin[0] == '_') {
      strcpy(*protocol, "gsi");
      strcpy(*host, &hostin[1]);
    } else {
      strcpy(*protocol, "tcp");
      strcpy(*host, hostin);
    }
  }
  for (i = strlen(*host) - 1; (*host)[i] == 32; i--) {
    (*host)[i] = 0;
    if (i == 0)
      break;
  }
}

////////////////////////////////////////////////////////////////////////////////
//  Do Login  //////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

///
/// Execute login inside server using given connection
///
/// \param id of connection (on client) to be used
/// \return status o login into server 1 if success, -1 if not authorized or error
/// occurred
///
static int DoLogin(int id)
{
  INIT_STATUS;
  Message *m;
  char *user_p;
#ifdef _WIN32
  char user[128];
  DWORD bsize = 128;
#ifdef _NI_RT_
  user_p = "Windows User";
#else
  user_p = GetUserName(user, &bsize) ? user : "Windows User";
#endif
#elif __MWERKS__
  user_p = "Macintosh User";
#else
#define BUFSIZE 256
  char buf[BUFSIZE];
  struct passwd pwd = {0};
  struct passwd *pwd_p = &pwd;
  getpwuid_r(geteuid(),&pwd,buf,BUFSIZE,&pwd_p);
  if (!pwd_p) {
#ifdef __APPLE__
    user_p = "Apple User";
#else
    /*
     *  On some RHEL6/64 systems 32 bit
     *  calls to getpwuid return 0
     *  temporary fix to call getlogin()
     *  in that case.
     */
    getlogin_r(buf,BUFSIZE);
    if (strlen(buf)>0)
      user_p = buf;
    else
      user_p = "Linux User";
#endif
  } else
    user_p = pwd_p->pw_name;
#endif
  unsigned int length = strlen(user_p);
  m = calloc(1, sizeof(MsgHdr) + length);
  m->h.client_type = SENDCAPABILITIES;
  m->h.length = (short)length;
  m->h.msglen = sizeof(MsgHdr) + length;
  m->h.dtype = DTYPE_CSTRING;
  m->h.status = GetConnectionCompression(id);
  m->h.ndims = 0;
  memcpy(m->bytes, user_p, length);
  status = SendMdsMsg(id, m, 0);
  free(m);
  if STATUS_OK {
    m = GetMdsMsg(id, &status);
    if (m == 0 || STATUS_NOT_OK) {
      printf("Error in connect\n");
      return MDSplusERROR;
    } else {
      if IS_NOT_OK(m->h.status) {
	printf("Error in connect: Access denied\n");
	free(m);
	return MDSplusERROR;
      }
      // SET CLIENT COMPRESSION FROM SERVER //
      SetConnectionCompression(id, (m->h.status & 0x1e) >> 1);
    }
    if (m)
      free(m);
  } else {
    perror("Error connecting to server");
    return MDSplusERROR;
  }
  return status;
}



////////////////////////////////////////////////////////////////////////////////
//  Reuse Check  ///////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

///
/// Trigger reuse check funcion for IoRoutines on host.
///
int ReuseCheck(char *hostin, char *unique, size_t buflen)
{
  int ok = -1;
  char *host = 0;
  char *protocol = 0;
  IoRoutines *io;
  ParseHost(hostin, &protocol, &host);
  io = LoadIo(protocol);
  if (io) {
    if (io->reuseCheck)
      ok = io->reuseCheck(host, unique, buflen);
    else {
      strncpy(unique, hostin, buflen);
      ok = 0;
    }
  } else
    memset(unique, 0, buflen);
  if (protocol)
    free(protocol);
  if (host)
    free(host);
  return ok;
}


////////////////////////////////////////////////////////////////////////////////
//  ConnectToMds  //////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////


int ConnectToMds(char *hostin)
{
  int id = -1;
  char *host = 0;
  char *protocol = 0;
  if (hostin == 0)
    return -1;
  ParseHost(hostin, &protocol, &host);
  id = NewConnection(protocol);
  if (id != -1) {
    IoRoutines *io;
    io = GetConnectionIo(id);
    if (io && io->connect) {
      SetConnectionCompression(id, GetCompressionLevel());
      if (io->connect(id, protocol, host) == -1) {
	DisconnectConnection(id);
	id = -1;
      } else if (DoLogin(id) == -1) {
	DisconnectConnection(id);
	id = -1;
      }
    }
  }
  if (host)
    free(host);
  if (protocol)
    free(protocol);
  return id;
}
