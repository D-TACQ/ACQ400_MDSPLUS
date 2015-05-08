/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * MARTE_XRAYSetup.java
 *
 * Created on Mar 2, 2011, 1:07:35 PM
 */

/**
 *
 * @author manduchi
 */
public class MARTE_XRAYSetup extends DeviceSetup {

    /** Creates new form MARTE_XRAYSetup */
    public MARTE_XRAYSetup() {
        initComponents();
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        deviceTableBeanInfo1 = new DeviceTableBeanInfo();
        deviceButtons1 = new DeviceButtons();
        jPanel2 = new javax.swing.JPanel();
        jPanel5 = new javax.swing.JPanel();
        deviceField1 = new DeviceField();
        jPanel6 = new javax.swing.JPanel();
        deviceField2 = new DeviceField();
        deviceField3 = new DeviceField();
        jPanel7 = new javax.swing.JPanel();
        deviceField4 = new DeviceField();
        deviceField5 = new DeviceField();
        jPanel8 = new javax.swing.JPanel();
        deviceChoice1 = new DeviceChoice();
        deviceField6 = new DeviceField();
        jPanel9 = new javax.swing.JPanel();
        deviceField7 = new DeviceField();
        deviceField8 = new DeviceField();
        jPanel1 = new javax.swing.JPanel();
        jTabbedPane1 = new javax.swing.JTabbedPane();
        jPanel10 = new javax.swing.JPanel();
        deviceTable1 = new DeviceTable();

        setDeviceProvider("localhost");
        setDeviceTitle("MARTe XRAY Setup");
        setDeviceType("MARTE_XRAY");
        setHeight(400);
        setWidth(600);
        getContentPane().add(deviceButtons1, java.awt.BorderLayout.PAGE_END);

        jPanel2.setLayout(new java.awt.GridLayout(5, 0));

        deviceField1.setIdentifier("");
        deviceField1.setLabelString("Comment: ");
        deviceField1.setNumCols(30);
        deviceField1.setOffsetNid(1);
        deviceField1.setTextOnly(true);
        jPanel5.add(deviceField1);

        jPanel2.add(jPanel5);

        deviceField2.setIdentifier("");
        deviceField2.setLabelString("Start Sampling(s):");
        deviceField2.setOffsetNid(8);
        jPanel6.add(deviceField2);

        deviceField3.setIdentifier("");
        deviceField3.setLabelString("End Sampling(s):");
        deviceField3.setOffsetNid(9);
        jPanel6.add(deviceField3);

        jPanel2.add(jPanel6);

        deviceField4.setIdentifier("");
        deviceField4.setLabelString("Start Offset Comp(s).:");
        deviceField4.setOffsetNid(6);
        jPanel7.add(deviceField4);

        deviceField5.setIdentifier("");
        deviceField5.setLabelString("End Offset Comp.(s):");
        deviceField5.setOffsetNid(7);
        jPanel7.add(deviceField5);

        jPanel2.add(jPanel7);

        deviceChoice1.setChoiceItems(new String[] {"XRayControl"});
        deviceChoice1.setIdentifier("");
        deviceChoice1.setLabelString("Control: ");
        deviceChoice1.setOffsetNid(12);
        deviceChoice1.setUpdateIdentifier("");
        jPanel8.add(deviceChoice1);

        deviceField6.setIdentifier("");
        deviceField6.setLabelString("Contr. Duration(s): ");
        deviceField6.setOffsetNid(5);
        jPanel8.add(deviceField6);

        jPanel2.add(jPanel8);

        deviceField7.setIdentifier("");
        deviceField7.setLabelString("Trig. Time: ");
        deviceField7.setNumCols(25);
        deviceField7.setOffsetNid(4);
        jPanel9.add(deviceField7);

        deviceField8.setIdentifier("");
        deviceField8.setLabelString("Freq. (Hz):");
        deviceField8.setOffsetNid(3);
        jPanel9.add(deviceField8);

        jPanel2.add(jPanel9);

        getContentPane().add(jPanel2, java.awt.BorderLayout.PAGE_START);

        jPanel1.setLayout(new java.awt.BorderLayout());

        jPanel10.setLayout(new java.awt.BorderLayout());

        deviceTable1.setColumnNames(new String[] {"Gain", "Offset"});
        deviceTable1.setDisplayRowNumber(true);
        deviceTable1.setIdentifier("");
        deviceTable1.setNumCols(2);
        deviceTable1.setNumRows(192);
        deviceTable1.setOffsetNid(10);
        deviceTable1.setUseExpressions(true);
        jPanel10.add(deviceTable1, java.awt.BorderLayout.CENTER);

        jTabbedPane1.addTab("In Calibration", jPanel10);

        jPanel1.add(jTabbedPane1, java.awt.BorderLayout.CENTER);

        getContentPane().add(jPanel1, java.awt.BorderLayout.CENTER);
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private DeviceButtons deviceButtons1;
    private DeviceChoice deviceChoice1;
    private DeviceField deviceField1;
    private DeviceField deviceField2;
    private DeviceField deviceField3;
    private DeviceField deviceField4;
    private DeviceField deviceField5;
    private DeviceField deviceField6;
    private DeviceField deviceField7;
    private DeviceField deviceField8;
    private DeviceTable deviceTable1;
    private DeviceTableBeanInfo deviceTableBeanInfo1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel10;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JPanel jPanel6;
    private javax.swing.JPanel jPanel7;
    private javax.swing.JPanel jPanel8;
    private javax.swing.JPanel jPanel9;
    private javax.swing.JTabbedPane jTabbedPane1;
    // End of variables declaration//GEN-END:variables

}
