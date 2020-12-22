import java.io.Serializable;

public class Device implements Serializable {

    private String devname;

    private String ipaddress;

    private String hostname;

    private String password;

    private DigitalTwin dtwin;

    public Device(String _devname, String _ipaddress, String _hostname, String _password) {
        this.devname = _devname;
        this.ipaddress = _ipaddress;
        this.hostname = _hostname;
        this.password = _password;
        this.dtwin = null;
    }

    public void print() {
        System.out.println("Device name: " + devname);
        System.out.println("Device ip address: " + ipaddress);
        System.out.println("Device hostname: " + hostname);
        System.out.println("Device password: " + password);
    }

    public String getIpaddress() {
        return ipaddress;
    }

    public String getDevname() {
        return devname;
    }

    public String getHostname() {
        return hostname;
    }

    public String getPassword() {
        return password;
    }

    public void setDtwin(DigitalTwin dtwin) {
        this.dtwin = dtwin;
    }

    public DigitalTwin getDtwin() {
        return dtwin;
    }
}