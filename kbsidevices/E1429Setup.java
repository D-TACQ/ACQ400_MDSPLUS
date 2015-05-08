/*
		A basic implementation of the DeviceSetup class.
                Korea Basic Science Institute(KBSI)
                Version 1.0
*/

import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class E1429Setup extends DeviceSetup
{
        static final int NID_ADDRESS = 1;
        static final int NID_SAMPLE_PERIOD = 4;
        static final int NID_SAMPLE_DELAY = 5;
        static final int NID_SAMPLE_SOURCE = 6;
        static final int NID_SAMPLE_NUM = 7;
        static final int NID_SAMPLE_NUMPRE = 8;
        static final int NID_TRIG_SOURCE = 10;
        static final int NID_TRIG_SLOPE = 11;
        static final int NID_TRIG_LEVEL = 12;
        static final int NID_TRIG_TTLOUT = 15;
        static final int NID_INPUT_RANGE = 18;
        static final int NID_INPUT_PORT = 19;
        public E1429Setup(Frame parent)
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
                setDeviceTitle("Agilient 2 ch 20 MSamples/s 12 bits digitizer");
//                setSize(600,400);
                Container contentPane = getContentPane();
		contentPane.setLayout(new GridBagLayout());
                GridBagConstraints c = new GridBagConstraints();

                jPanel = new JPanel();
                address.setNumCols(15);
                address.setTextOnly(true);
                address.setLabelString("Address:");
                address.setOffsetNid(NID_ADDRESS);
                jPanel.add(address);
                c.gridy = 0;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setLayout(new GridLayout(2,4));
                jPanel.setBorder(new TitledBorder("Input"));
                {
                        String[] tempString = new String[10];
                        tempString[0] = ".1 V";
                        tempString[1] = ".2 V";
                        tempString[2] = ".5 V";
                        tempString[3] = "1 V";
                        tempString[4] = "2 V";
                        tempString[5] = "5 V";
                        tempString[6] = "10 V";
                        tempString[7] = "20 V";
                        tempString[8] = "50 V";
                        tempString[9] = "100 V";
                        double range[] = {.1, .2, .5, 1., 2., 5., 10., 20., 50., 100.};
                        for (i=0; i<2; i++) {
                          ch[i] = new DeviceChoice();
                          ch[i].setChoiceItems(tempString);
                          ch[i].setChoiceDoubleValues(range);
                          ch[i].setLabelString("Ch "+i);
                          ch[i].setOffsetNid(NID_INPUT_RANGE + 6*i);
                          jPanel.add(ch[i]);
                        }
                }
                {
                        String[] tempString = new String[2];
                        tempString[0] = "Single Ended";
                        tempString[1] = "Differential";
                        for (i=0; i<2; i++) {
                          port[i] = new DeviceChoice();
                          port[i].setChoiceItems(tempString);
                          port[i].setConvert(true);
                          port[i].setLabelString("Port "+i);
                          port[i].setOffsetNid(NID_INPUT_PORT + 6*i);
                          jPanel.add(port[i]);
                        }
                }
                c.gridy = 1;
                c.gridheight = 2;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setBorder(new TitledBorder("   ##Samples Max :262,144 ,   ##Pre-trig : 0 ~ 65,535  ,  ##Delay : 0 ~ 65534T(T=0.05us), 65540T ~ 655,350T(in steps of 10T) "));
		sampleNum.setNumCols(4);
		sampleNum.setOffsetNid(NID_SAMPLE_NUM);
		sampleNum.setLabelString("# of Samples:");
		jPanel.add(sampleNum);

		sampleNumPre.setNumCols(4);
		sampleNumPre.setOffsetNid(NID_SAMPLE_NUMPRE);
		sampleNumPre.setLabelString("# of Pre Trigger:");
		jPanel.add(sampleNumPre);

                sampleDelay.setNumCols(4);
                sampleDelay.setOffsetNid(NID_SAMPLE_DELAY);
                sampleDelay.setLabelString("Delay");
                jPanel.add(sampleDelay);

                {
                        String[] tempString = new String[23];
                        tempString[0] = "20 MSa/sec";
                        tempString[1] = "10 MSa/sec";
                        tempString[2] = "5 MSa/sec";
                        tempString[3] = "2 MSa/sec";
                        tempString[4] = "1 MSa/sec";
                        tempString[5] = "500 kSa/sec";
                        tempString[6] = "200 kSa/sec";
                        tempString[7] = "100 kSa/sec";
                        tempString[8] = "50 kSa/sec";
                        tempString[9] = "20 kSa/sec";
                        tempString[10] = "10 kSa/sec";
                        tempString[11] = "5 kSa/sec";
                        tempString[12] = "2 kSa/sec";
                        tempString[13] = "1 kSa/sec";
                        tempString[14] = "500 Sa/sec";
                        tempString[15] = "200 Sa/sec";
                        tempString[16] = "100 Sa/sec";
                        tempString[17] = "50 Sa/sec";
                        tempString[18] = "20 Sa/sec";
                        tempString[19] = "10 Sa/sec";
                        tempString[20] = "5 Sa/sec";
                        tempString[21] = "2 Sa/sec";
                        tempString[22] = "1 Sa/sec";
                        double period[] = {0.5e-7, 0.1e-6, 0.2e-6, 0.5e-6, 0.1e-5, 0.2e-5, 0.5e-5, 0.1e-4,
                            0.2e-4, 0.5e-4, 0.1e-3, 0.2e-3, 0.5e-3, 0.1e-2, 0.2e-2, 0.5e-2, 0.1e-1,
                            0.2e-1, 0.5e-1, 0.1, 0.2, 0.5, 1.0};
                        samplePeriod.setChoiceItems(tempString);
                        samplePeriod.setChoiceDoubleValues(period);
                        samplePeriod.setLabelString("Period:");
//                        samplePeriod.setShowState(true);
                        samplePeriod.setOffsetNid(NID_SAMPLE_PERIOD);
                        jPanel.add(samplePeriod);
                }

                {
                    String[] tempString = new String[19];
                    tempString[0] = "Bus";
                    tempString[1] = "Hold";
                    tempString[2] = "ECLTrg 0";
                    tempString[3] = "ECLTrg 1";
                    tempString[4] = "TTLTrg 0";
                    tempString[5] = "TTLTrg 1";
                    tempString[6] = "TTLTrg 2";
                    tempString[7] = "TTLTrg 3";
                    tempString[8] = "TTLTrg 4";
                    tempString[9] = "TTLTrg 5";
                    tempString[10] = "TTLTrg 6";
                    tempString[11] = "TTLTrg 7";
                    tempString[12] = "External 1";
                    tempString[13] = "External 2";
                    tempString[14] = "Timer";
                    tempString[15] = "Dual External";
                    tempString[16] = "Dual ECL Trig";
                    tempString[17] = "Dual Timer";
                    tempString[18] = "VME";
                    sampleSource.setChoiceItems(tempString);
                    sampleSource.setConvert(true);
                    sampleSource.setLabelString("source:");
                    sampleSource.setOffsetNid(NID_SAMPLE_SOURCE);
                }
                jPanel.add(sampleSource);

                c.gridy = 3;
                c.gridheight = 1;
                contentPane.add(jPanel, c);

	jPanel = new JPanel();
        jPanel.setBorder(new TitledBorder("Triggering"));
		{
			String[] tempString = new String[16];
			tempString[0] = "Bus";
			tempString[1] = "Hold";
			tempString[2] = "ECLTrg 0";
                        tempString[3] = "ECLTrg 1";
                        tempString[4] = "TTLTrg 0";
                        tempString[5] = "TTLTrg 1";
                        tempString[6] = "TTLTrg 2";
                        tempString[7] = "TTLTrg 3";
                        tempString[8] = "TTLTrg 4";
                        tempString[9] = "TTLTrg 5";
                        tempString[10] = "TTLTrg 6";
                        tempString[11] = "TTLTrg 7";
                        tempString[12] = "External";
                        tempString[13] = "Internal 0";
                        tempString[14] = "Internal 1";
                        tempString[15] = "Immediate";
			trigSource.setChoiceItems(tempString);
                        trigSource.setConvert(true);
                        trigSource.setLabelString("Source:");
                        trigSource.setOffsetNid(NID_TRIG_SOURCE);
		}
		jPanel.add(trigSource);

                {
                        String[] tempString = new String[3];
                        tempString[0] = "Positive";
                        tempString[1] = "Negative";
                        tempString[2] = "Either";
                        trigSlope.setChoiceItems(tempString);
                        trigSlope.setConvert(true);
                        trigSlope.setLabelString("Slope:");
                        trigSlope.setOffsetNid(NID_TRIG_SLOPE);
                }
                jPanel.add(trigSlope);

                trigLevel.setNumCols(4);
                trigLevel.setLabelString("Level:");
                trigLevel.setOffsetNid(NID_TRIG_LEVEL);
                jPanel.add(trigLevel);

                c.gridy = 4;
                contentPane.add(jPanel, c);

                jPanel = new JPanel();
                jPanel.setBorder(new TitledBorder("Output TTL pulses"));
                ttlOut.setNumCols(4);
                ttlOut.setOffsetNid(NID_TRIG_TTLOUT);
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

	public E1429Setup()
	{
		this((Frame)null);
	}

	public E1429Setup(String sTitle)
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
		(new E1429Setup()).setVisible(true);
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
	DeviceChoice samplePeriod = new DeviceChoice();
	DeviceField sampleNum = new DeviceField();
        DeviceField sampleNumPre = new DeviceField();
        DeviceField sampleDelay = new DeviceField();
	DeviceChoice sampleSource = new DeviceChoice();
        DeviceChoice trigSlope = new DeviceChoice();
        DeviceField trigLevel = new DeviceField();
	DeviceChoice trigSource = new DeviceChoice();
	DeviceField ttlOut = new DeviceField();
	DeviceChoice ch[] = new DeviceChoice[2];
        DeviceChoice port[] = new DeviceChoice[2];
	DeviceField address = new DeviceField();
	//}}

}
