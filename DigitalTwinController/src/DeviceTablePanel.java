

import javax.swing.*;
import java.awt.*;

public class DeviceTablePanel extends JPanel {
    private DtControllerGUI frame;

    private JTable table;

    private JButton addButton;

    private JButton removeButton;

    private JButton viewDataButton;

    private JButton generateAndDeployButton;


    public DeviceTablePanel(DtControllerGUI gui) {
        this.setLayout(new BorderLayout());
        this.frame = gui;
        this.setLayout(new BorderLayout(5, 5));
        addButton = new JButton("Add new device");
        addButton.setEnabled(true);

        removeButton = new JButton("Remove device");
        removeButton.setEnabled(false);

        viewDataButton = new JButton("View data");
        viewDataButton.setEnabled(false);

        generateAndDeployButton = new JButton("Generate and deploy DT");
        generateAndDeployButton.setEnabled(false);

        DeviceTableModel model = new DeviceTableModel(frame.controller.getDevices());
        table = new JTable();
        table.setFillsViewportHeight(true);
        table.setModel(model);
        table.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                int row = table.rowAtPoint(evt.getPoint());

            }
        });
        JScrollPane pane = new JScrollPane(table);

        this.add(pane, BorderLayout.NORTH);
        this.add(addButton, BorderLayout.SOUTH);
        this.add(removeButton, BorderLayout.SOUTH);
        this.add(viewDataButton, BorderLayout.SOUTH);
        this.add(generateAndDeployButton, BorderLayout.SOUTH);

    }
}
