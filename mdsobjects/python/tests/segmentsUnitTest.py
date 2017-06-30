from unittest import TestCase,TestSuite
from MDSplus import Tree,Float32,Float32Array,Int16Array,setenv,makeArray
from threading import Lock

class segmentsTests(TestCase):
    _lock      = Lock()
    _instances = 0
    _tmpdir    = None

    @classmethod
    def setUpClass(cls):
        with cls._lock:
            if cls._instances == 0:
                import tempfile
                cls._tmpdir=tempfile.mkdtemp()
            setenv("seg_tree_path",cls._tmpdir)
            cls._instances+=1
    @classmethod
    def tearDownClass(cls):
        import gc,shutil
        gc.collect()
        with cls._lock:
            cls._instances -= 1
            if not cls._instances>0:
                shutil.rmtree(cls._tmpdir)

    def arrayDimensionOrder(self):
        from numpy import int16,zeros
        from random import randint
        ptree=Tree('seg_tree',-1,'NEW')
        ptree.addNode('IMM')
        ptree.write()
        ptree=Tree('seg_tree',-1)
        ptree.createPulse(1)
        ptree=Tree('seg_tree',1)
        node=ptree.getNode('IMM')
        WIDTH = 640
        HEIGHT= 480;
        currFrame=zeros(WIDTH*HEIGHT, dtype = int16);
        currTime=float(0);
        for i in range(0,WIDTH):
            for j in range(0,HEIGHT):
                currFrame[i*HEIGHT+j]=randint(0,255)
        currTime = float(0)
        startTime = Float32(currTime)
        endTime = Float32(currTime)
        dim = Float32Array(currTime)
        segment = Int16Array(currFrame)
        segment.resize([1,HEIGHT,WIDTH])
        shape = segment.getShape()
        node.makeSegment(startTime, endTime, dim, segment)
        retShape = node.getShape()
        self.assertEqual(shape[0],retShape[0])
        self.assertEqual(shape[1],retShape[1])
        self.assertEqual(shape[2],retShape[2])

    def writeSegments(self):
        from numpy import array,zeros,int32
        ptree = Tree('seg_tree',-1,'NEW')
        ptree.addNode('MS')
        ptree.addNode('MS_MD')
        ptree.addNode('MTS')
        ptree.addNode('MTS_MD')
        ptree.addNode('PS')
        ptree.addNode('PR')
        ptree.addNode('PTS')
        ptree.write()
        ptree = Tree('seg_tree',-1)
        length,width = 16,7
        dim = [2*i+2 for i in range(length)]        # shape (16)
        dat = [[i*width+j+1 for j in range(width)] for i in range(length)]  # shape (16,7)
        ndim,ndat = array(dim,int32),array(dat,int32)
        ### makeSegment ###
        node = ptree.MS
        seglen = 1
        for i in range(0,length,seglen):
            node.makeSegment(dim[i]-1,dim[i+seglen-1]+1,ndim[i:i+seglen],ndat[i:i+seglen])
        self.assertEqual(node.getSegmentLimits(1),(3,5))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### makeSegment multidim ###
        node = ptree.MS_MD
        seglen = 4
        for i in range(0,length,seglen):
            node.makeSegment(dim[i]-1,dim[i+seglen-1]+1,ndim[i:i+seglen],ndat[i:i+seglen])
        self.assertEqual(node.getSegmentLimits(1),(9,17))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### makeTimestampedSegment ###
        node = ptree.MTS
        seglen = 1
        for i in range(0,length,seglen):
            node.makeTimestampedSegment(ndim[i:i+seglen],ndat[i:i+seglen],-1,seglen)
        self.assertEqual(node.getSegmentLimits(1),(4,4))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### makeTimestampedSegment multidim ###
        node = ptree.MTS_MD
        seglen = 4
        for i in range(0,length,seglen):
            node.makeTimestampedSegment(ndim[i:i+seglen],ndat[i:i+seglen],-1,seglen)
        self.assertEqual(node.getSegmentLimits(1),(10,16))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### putSegment ###
        node = ptree.PS
        seglen = 4
        segbuf = zeros((int(length/seglen),width),int32)
        for i in range(0,length,seglen):
            node.beginSegment(dim[i]-1,dim[i+seglen-1]+1,ndim[i:i+seglen],segbuf)
            for j in range(seglen):
                node.putSegment(ndat[i+j:i+j+1],j)
        self.assertEqual(node.getSegmentLimits(1),(9,17))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### putRow ###
        node = ptree.PR
        seglen = 4
        segbuf = zeros((int(length/seglen),width),int32)
        for i in range(0,length,seglen):
            node.beginTimestampedSegment(segbuf)
            for j in range(seglen):
                node.putRow(64,ndat[i+j:i+j+1],dim[i+j])
        self.assertEqual(node.getSegmentLimits(1),(10,16))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)
        ### putTimestampedSegment ###
        node = ptree.PTS
        seglen = 4
        for i in range(0,length,seglen):
            node.beginTimestampedSegment(segbuf)
            for j in range(seglen):
                node.putTimestampedSegment(dim[i+j:i+j+1],ndat[i+j:i+j+1])
        self.assertEqual(node.getSegmentLimits(1),(10,16))
        self.assertEqual(node.record.dim_of().tolist(),dim)
        self.assertEqual(node.record.data().tolist(),dat)

    def runTest(self):
        for test in self.getTests():
            self.__getattribute__(test)()
    @staticmethod
    def getTests():
        return ['arrayDimensionOrder','writeSegments']
    @classmethod
    def getTestCases(cls):
        return map(cls,cls.getTests())

def suite():
    return TestSuite(segmentsTests.getTestCases())

def run():
    from unittest import TextTestRunner
    TextTestRunner(verbosity=10).run(suite())

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1].lower()=="objgraph":
        import objgraph
    else:      objgraph = None
    import gc;gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
    run()
    if objgraph:
         gc.collect()
         objgraph.show_backrefs([a for a in gc.garbage if hasattr(a,'__del__')],filename='%s.png'%__file__[:-3])
