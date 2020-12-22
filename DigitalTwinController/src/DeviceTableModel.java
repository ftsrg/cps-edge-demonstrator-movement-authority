import javax.swing.table.AbstractTableModel;
import java.lang.reflect.Array;
import java.util.ArrayList;

public class DeviceTableModel extends AbstractTableModel {

    public ArrayList<Device> devices;

    public DeviceTableModel(ArrayList<Device> _devices) {
        devices = new ArrayList<>();
        devices = _devices;
    }

    @Override
    public int getRowCount() {
        return devices.size();
    }

    @Override
    public int getColumnCount() {
        return 6;
    }

    @Override
    public String getColumnName(int column) {
        switch (column) {
            case 0:
                return "Device name";
            case 1:
                return "Device IP";
            case 2:
                return "Device hostname";
            case 3:
                return "Device password";
            case 4:
                return "Thing ID";
            default:
                return "Digital Twin State";
        }
    }

    @Override
    public Object getValueAt(int i, int i1) {
        Device d = devices.get(i);
        switch (i1) {
            case 0:
                return d.getDevname();
            case 1:
                return d.getIpaddress();
            case 2:
                return d.getHostname();
            case 3:
                return d.getPassword();
            case 4:
                return d.getDtwin() == null ? "No Digital Twin" : d.getDtwin().getThingID();
            default:
                return d.getDtwin() == null ? "No digital Twin" : d.getDtwin().isRunning() ? "Running" : "Not running";
        }
    }

    public boolean addDevice(Device d) {
        if (devices.contains(d)) {

            return false;
        } else {
            devices.add(d);
            fireTableRowsInserted(devices.size() - 1, devices.size() - 1);
            return true;
        }
    }

    @Override
    public Class<?> getColumnClass(int columnIndex) {
        switch (columnIndex) {
            default:
                return String.class;
        }
    }

    public void deleteDevice(int index) {
        devices.remove(index);
        fireTableRowsDeleted(index, index);
    }
}
