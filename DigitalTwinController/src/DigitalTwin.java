import java.io.Serializable;
import java.util.Map;

public class DigitalTwin implements Serializable {

    private String namespace;

    private String name;

    private String thingID;

    private Map<String, String> datas;

    private boolean running = false;

    public DigitalTwin(String _namespace, String _name, Map<String, String> _datas) {
        this.namespace = _namespace;
        this.name = _name;
        this.datas = _datas;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String getNamespace() {
        return namespace;
    }

    public String getThingID() {
        return thingID;
    }

    public void setThingID(String thingID) {
        this.thingID = thingID;
    }

    public Map<String, String> getDatas() {
        return datas;
    }

    public void setDatas(Map<String, String> datas) {
        this.datas = datas;
    }

    public void setNamespace(String namespace) {
        this.namespace = namespace;
    }

    public void setRunning(boolean running) {
        this.running = running;
    }

    public boolean isRunning() {
        return running;
    }
}
