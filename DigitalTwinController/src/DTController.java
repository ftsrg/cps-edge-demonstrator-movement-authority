import jdk.nashorn.internal.parser.JSONParser;

import javax.swing.table.TableModel;
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class DTController {
    private ArrayList<Device> devices;

    private DeviceTableModel model;

    public DTController() {
        devices = new ArrayList<>();
        try {
            loadDevices();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        model = new DeviceTableModel(devices);

    }

    public void loadDevices() throws ClassNotFoundException {
        try {
            FileInputStream devicefile = new FileInputStream("devices");
            ObjectInputStream deviceinput = new ObjectInputStream(devicefile);

            devices = (ArrayList<Device>) deviceinput.readObject();

            deviceinput.close();
            devicefile.close();
        } catch (EOFException x){
            System.out.println("üres a fájl");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void saveDevices() {
        try {
            FileOutputStream devicefile = new FileOutputStream("devices");
            ObjectOutputStream deviceoutput = new ObjectOutputStream(devicefile);

            deviceoutput.writeObject(devices);

            deviceoutput.close();
            devicefile.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void printAllDevice() {
        if (devices.size() == 0) {
            System.out.print("There is no device");
        } else {
            for (Device d : devices) {
                d.print();
            }
        }
    }

    public String checkConnection(int index) {
        String path = System.getProperty("user.dir") + "/checksshv2.py";
        Device d = devices.get(index);
        boolean failed = false;
        try {
            ProcessBuilder pb = new ProcessBuilder("python3", path, d.getIpaddress(), d.getHostname(), d.getPassword());
            Process p = pb.start();

            BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = "";
            while ((line = bfr.readLine()) != null) {
                return line;
            }
            int code = p.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public ArrayList<Map<String, String>> preprocess(String filepath, int selected) {
        String path = System.getProperty("user.dir") + "/genFromDSL-preprocess.py";
        Device d = devices.get(selected);

        Map<String, String> datas = new HashMap<>();
        Map<String, String> functiontodata = new HashMap<>();
        try {
            ProcessBuilder pb = new ProcessBuilder("python3", path, filepath);
            Process p = pb.start();

            BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = "";
            boolean data = false;
            boolean operations = false;
            boolean namespace = false;
            boolean infomodel = false;
            String ns = "";
            String imodel = "";
            String functionblock = "";
            while ((line = bfr.readLine()) != null) {
                if (line.contains("[NAMESPACE]")) {
                    namespace = true;
                    continue;
                }
                if (line.contains("[IMODEL]")) {
                    namespace = false;
                    infomodel = true;
                    continue;
                }
                if (line.contains("[DATA]")) {
                    infomodel = false;
                    data = true;
                    continue;
                }
                if (line.contains("[OPERATIONS]")) {
                    data = false;
                    operations = true;
                    continue;
                }
                if (namespace) {
                    ns = line;
                }
                if (infomodel) {
                    imodel = line;
                }
                if (data) {

                    if (line.contains("Functionblock")) {
                        functionblock = line.split(" ")[1];
                        continue;
                    }
                    functiontodata.put(line.split(" ")[0], functionblock);
                    datas.put(line.split(" ")[0], line.split(" ")[1]);

                }
                if (operations) {
                }

            }
            d.setDtwin(new DigitalTwin(ns, imodel, datas));
            int code = p.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        ArrayList<Map<String, String>> ret = new ArrayList<>();
        ret.add(datas);
        ret.add(functiontodata);
        return ret;
    }

    public void generate(ArrayList<String> sendables, int selected, String text) {
        String path = System.getProperty("user.dir") + "/genFromDSL-generate.py";

        String[] commandlist = {"python3", path};
        Device d = devices.get(selected);
        ArrayList<String> sending = new ArrayList<>();
        sending.add("python3");
        sending.add(path);
        sending.add(d.getDtwin().getThingID());
        sending.add(d.getDevname());
        sending.add(d.getDtwin().getNamespace());
        sending.add(text);
        for (String s : sendables) {
            sending.add(s);
        }
        ProcessBuilder pb = new ProcessBuilder(sending.toArray(new String[sendables.size() + 2]));
        try {
            Process p = pb.start();
            int code = p.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }


    }

    public Map<String, String> gethttp(String command, Map<String, String> data) {
        String[] properties = data.keySet().toArray(new String[data.size()]);

        Map<String, String> returndata = new HashMap<>();
        ProcessBuilder pb = new ProcessBuilder(command.split(" "));
        try {
            Process p = pb.start();
            BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = "";
            String[] sliced = new String[0];
            ArrayList<String> rows = new ArrayList<>();
            while ((line = bfr.readLine()) != null) {
                sliced = line.split(",");
                for (String s : sliced) {
                    rows.add(s);
                }
            }
            rows.remove(0);
            rows.remove(0);
            rows.remove(0);
            rows.remove(0);

            for (String s : rows) {
                String[] splitted = s.split("\"");
                for (int i = 0; i < splitted.length; i++) {
                    if (data.containsKey(splitted[i])) {
                        returndata.put(splitted[i], splitted[++i].replace(":", "").replace("}", ""));
                    }
                }
            }
            int code = p.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return returndata;
    }

    public void deploy(String devicename, String targetdir) {
        String command1 = "fab2 transfer --file " + System.getProperty("user.dir") + "/generated/" + devicename + "/DeviceWriter.py --targetdir " + targetdir;
        ProcessBuilder pb = new ProcessBuilder(command1.split(" "));
        String command2 = "fab2 transfer --file " + System.getProperty("user.dir") + "/generated/" + devicename + "/Every.xml --targetdir " + targetdir;
        ProcessBuilder pb2 = new ProcessBuilder(command2.split(" "));
        try {
            Process p = pb.start();
            int code = p.waitFor();
            p = pb2.start();
            int code1 = p.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
        }


    }

    public ArrayList<Device> getDevices() {
        return devices;
    }

    public boolean addDevice(Device d) {
        return model.addDevice(d);
    }

    public void removeDevice(int index) {
        model.deleteDevice(index);
    }

    public TableModel getTableModel() {
        return model;
    }

    public void run(int selected) {
        Device d = devices.get(selected);
        ProcessBuilder pb = new ProcessBuilder("node", System.getProperty("user.dir") + "/generated/" + d.getDevname() + "/AllReader.js");

        ProcessBuilder pb1 = new ProcessBuilder("fab2", "runremote");
        try {
            Process p = pb.start();
            Process p2 = pb1.start();
            d.getDtwin().setRunning(true);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stopprocess(int selected) {
        Device d = devices.get(selected);
        ProcessBuilder pb = new ProcessBuilder("fab2", "stoplocal");
        ProcessBuilder pb1 = new ProcessBuilder("fab2", "stopremote");
        try {
            Process p = pb.start();
            Process p2 = pb1.start();
            d.getDtwin().setRunning(false);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
