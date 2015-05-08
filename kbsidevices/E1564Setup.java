/*
		A basic implementation of the DeviceSetup class.
                Korea Basic Science Institute(KBSI)
                Version 1.0
*/

import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class E1564Setup extends DeviceSetup
{
                public E1564Setup(Frame parent)
	{
	super(parent);
          int i;
          JPanel jPanel;
		// This code is automatically generated by Visual Cafe when you add
		// components to the visual environment. It instantiates and initializes
		// the components. To modify the code, only use code syntax that matches
		// what Visual Cafe can generate, or Visual Cafe may be unable to back
		// parse your Java file into its visual environment.
		//{{INIT_CONTROLS
                setDeviceTitle("Agilient 4 ch 800 kSamples/s 14 bits digitizer");
//                setSize(600,400);
                Container contentPane = getContentPane();
		contentPane.setLayout(new GridBagLayout());
                GridBagConstraints c = new GridBagConstraints();

                jPanel = new JPanel();
                address.setNumCols(15);
                address.setTextOnly(true);
                address.setLabelString("Address:");
                address.setOffsetNid(1);
                jPanel.add(address);
                c.gridy = 0;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setLayout(new GridLayout(2,4));
                jPanel.setBorder(new TitledBorder("Input"));
                {
                        String[] tempString = new String[7];
                        tempString[0] = ".0625 V";
                        tempString[1] = ".25 V";
                        tempString[2] = "1 V";
                        tempString[3] = "4 V";
                        tempString[4] = "16 V";
                        tempString[5] = "64 V";
                        tempString[6] = "256 V";
                        double range[] = {.0625, .25, 1., 4., 16., 64., 256.};
                        for (i=0; i<4; i++) {
                          ch[i] = new DeviceChoice();
                          ch[i].setChoiceItems(tempString);
                          ch[i].setChoiceDoubleValues(range);
                          ch[i].setLabelString("Ch "+i);
                          ch[i].setOffsetNid(16 + 6*i);
                          jPanel.add(ch[i]);
                        }
                }
                {
                        String[] tempString = new String[5];
                        tempString[0] = "OFF";
                        tempString[1] = "1.5 kHz";
                        tempString[2] = "6 kHz";
                        tempString[3] = "25 kHz";
                        tempString[4] = "100 kHz";
                        double cutoff[] = {0., 1500., 6000., 25000., 100000.};
                        for (i=0; i<4; i++) {
                          filter[i] = new DeviceChoice();
                          filter[i].setChoiceItems(tempString);
                          filter[i].setChoiceDoubleValues(cutoff);
                          filter[i].setLabelString("Filter "+i);
                          filter[i].setOffsetNid(17 + 6*i);
                          jPanel.add(filter[i]);
                        }
                }
                c.gridy = 1;
                c.gridheight = 2;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setBorder(new TitledBorder("# Sampling Max : 2,096,151(16M-4CH) , # Pre- Trigger : sample count -1 , # Period (4ch): 800kSample/s"));
		sampleNum.setNumCols(4);
		sampleNum.setOffsetNid(6);
		sampleNum.setLabelString("# of Samples:");
		jPanel.add(sampleNum);

		sampleNumPre.setNumCols(4);
		sampleNumPre.setOffsetNid(7);
		sampleNumPre.setLabelString("# of Pre Trigger:");
		jPanel.add(sampleNumPre);

                samplePeriod.setNumCols(4);
                samplePeriod.setOffsetNid(4);
                samplePeriod.setLabelString("Period:");
                jPanel.add(samplePeriod);

                {
                    String[] tempString = new String[12];
                    tempString[0] = "Wait for Software sample";
                    tempString[1] = "Timer";
                    tempString[2] = "TTLTrg0";
                    tempString[3] = "TTLTrg1";
                    tempString[4] = "TTLTrg2";
                    tempString[5] = "TTLTrg3";
                    tempString[6] = "TTLTrg4";
                    tempString[7] = "TTLTrg5";
                    tempString[8] = "TTLTrg6";
                    tempString[9] = "TTLTrg7";
                    tempString[10] = "External Rising Edge";
                    tempString[11] = "External Rising Edge";
                    sampleSource.setChoiceItems(tempString);
                    sampleSource.setConvert(true);
                    sampleSource.setLabelString("source:");
                    sampleSource.setOffsetNid(5);
                }
                jPanel.add(sampleSource);

                c.gridy = 3;
                c.gridheight = 1;
                contentPane.add(jPanel, c);

	jPanel = new JPanel();
        jPanel.setBorder(new TitledBorder("Triggering"));
		{
			String[] tempString = new String[21];
			tempString[0] = "Bus";
			tempString[1] = "External Falling Edge";
			tempString[2] = "External Rising Edge";
                        tempString[3] = "Wait for Software trigger";
                        tempString[4] = "Immediate";
                        tempString[5] = "Falling below chan 1 level";
                        tempString[6] = "Rising above chan 1 level";
                        tempString[7] = "Falling below chan 2 level";
                        tempString[8] = "Rising above chan 2 level";
                        tempString[9] = "Falling below chan 3 level";
                        tempString[10] = "Rising above chan 3 level";
                        tempString[11] = "Falling below chan 4 level";
                        tempString[12] = "Rising above chan 4 level";
                        tempString[13] = "TTLTrg0";
                        tempString[14] = "TTLTrg1";
                        tempString[15] = "TTLTrg2";
                        tempString[16] = "TTLTrg3";
                        tempString[17] = "TTLTrg4";
                        tempString[18] = "TTLTrg5";
                        tempString[19] = "TTLTrg6";
                        tempString[20] = "TTLTrg7";
			trigSource.setChoiceItems(tempString);
                        trigSource.setConvert(true);
                        trigSource.setLabelString("Source:");
                        trigSource.setOffsetNid(9);
		}
		jPanel.add(trigSource);

                trigLevel.setNumCols(4);
                trigLevel.setLabelString("Level:");
                trigLevel.setOffsetNid(10);
                jPanel.add(trigLevel);

                c.gridy = 4;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setBorder(new TitledBorder("Output TTL pulses"));
                ttlOut.setNumCols(4);
                ttlOut.setOffsetNid(13);
                ttlOut.setLabelString("TTL");
                jPanel.add(ttlOut);
                c.gridy = 5;
                contentPane.add(jPanel, c);

                c.gridy = 6;
                contentPane.add(dispatch, c);
                {
                        String[] tempString = new String[3];
                        tempString[0] = "INIT";
                        tempString[1] = "ARM";
                        tempString[2] = "STORE";
                        deviceButtons.setMethods(tempString);
                }
                c.gridy = 7;
                contentPane.add(deviceButtons, c);
                pack();
		//}}
	}

	public E1564Setup()
	{
		this((Frame)null);
	}

	public E1564Setup(String sTitle)
	{
		this();
		setTitle(sTitle);
	}

	public void setVisible(boolean b)
	{
		if (b)
			setLocation(50, 50);
		super.setVisible(b);
	}

	static public void main(String args[])
	{
		(new E1564Setup()).setVisible(true);
	}

	public void addNotify()
	{
		// Record the size of the window prior to calling parents addNotify.
		Dimension size = getSize();

		super.addNotify();

		if (frameSizeAdjusted)
			return;
		frameSizeAdjusted = true;

		// Adjust size of frame according to the insets
		Insets insets = getInsets();
		setSize(insets.left + insets.right + size.width, insets.top + insets.bottom + size.height);
	}

	// Used by addNotify
	boolean frameSizeAdjusted = false;

	//{{DECLARE_CONTROLS
	DeviceButtons deviceButtons = new DeviceButtons();
	DeviceDispatch dispatch = new DeviceDispatch();
	DeviceField samplePeriod = new DeviceField();
	DeviceField sampleNum = new DeviceField();
        DeviceField sampleNumPre = new DeviceField();
	DeviceChoice sampleSource = new DeviceChoice();
	DeviceField trigLevel = new DeviceField();
	DeviceChoice trigSource = new DeviceChoice();
	DeviceField ttlOut = new DeviceField();
	DeviceChoice ch[] = new DeviceChoice[4];
        DeviceChoice filter[] = new DeviceChoice[4];
	DeviceField address = new DeviceField();
	//}}

}