import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class DataPanel extends JPanel {
    private JPanel panel = this;
    private DTController controller;
    private DtControllerGUI frame;
    private ArrayList<JLabel> displayvalues = new ArrayList<>();
    boolean cancelled = false;

    public DataPanel(DTController controller, DtControllerGUI frame, JPanel controlPanel) {
        this.controller = controller;
        this.frame = frame;
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.NORTHWEST;
        JButton cancelBtn = new JButton("Cancel");
        gbc.gridx = 1;
        gbc.anchor = GridBagConstraints.NORTHEAST;
        JButton refreshButton = new JButton("Refresh");
        refreshButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                refreshPanel();
            }
        });
        add(cancelBtn, gbc);
        add(refreshButton, gbc);
        cancelBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                frame.remove(panel);
                frame.add(controlPanel, BorderLayout.CENTER);
                cancelled = true;
                frame.revalidate();
                frame.repaint();
            }
        });
        JPanel dataPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbcdata = new GridBagConstraints();
        int y = 0;
        for (String s : controller.getDevices().get(frame.getSelected()).getDtwin().getDatas().keySet()) {
            gbcdata.gridx = 0;
            gbcdata.gridy = y++;
            gbcdata.anchor = GridBagConstraints.NORTHWEST;
            dataPanel.add(new JLabel(s), gbcdata);
        }
        String command = "curl -X GET -u ditto:ditto http://localhost:8080/api/1/things/" + controller.getDevices().get(frame.getSelected()).getDtwin().getNamespace() + ":" + controller.getDevices().get(frame.getSelected()).getDtwin().getThingID();

        Map<String, String> displaymap = controller.gethttp(command, controller.getDevices().get(frame.getSelected()).getDtwin().getDatas());
        y = 0;

        for (String key : displaymap.keySet()) {
            gbcdata.gridx = 1;
            gbcdata.gridy = y++;
            gbcdata.anchor = GridBagConstraints.NORTHEAST;
            JLabel value = new JLabel(displaymap.get(key));
            displayvalues.add(value);
            dataPanel.add(value, gbcdata);
        }

        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.CENTER;
        add(dataPanel, gbc);
    }

    public void refreshPanel() {
        Map<String, String> display = controller.gethttp("curl -X GET -u ditto:ditto http://localhost:8080/api/1/things/" + controller.getDevices().get(frame.getSelected()).getDtwin().getNamespace() + ":" + controller.getDevices().get(frame.getSelected()).getDtwin().getThingID(), controller.getDevices().get(frame.getSelected()).getDtwin().getDatas());
        int index = 0;
        for (String s : display.keySet()) {
            displayvalues.get(index).setText(display.get(s));
            index++;
        }
        validate();
        repaint();


    }
}
