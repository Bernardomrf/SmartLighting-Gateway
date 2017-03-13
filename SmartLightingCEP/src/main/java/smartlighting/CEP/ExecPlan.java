/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.CEP;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import java.util.ArrayList;
import java.util.Map;
import java.util.regex.Pattern;
import smartlighting.Resources.Adapters;

/**
 *
 * @author bernardo
 */
public class ExecPlan {
    
    private String ep;
    private Map<String, Object> json;
    private Adapters redis;
    
    public ExecPlan(String ep, String json){
        loadJson(json);
        loadEP(ep);
        
    }
    
    private void loadEP(String ep){
        this.ep = ep;
    }
    
    public String getEP(){
        
        return ep;
    }
    
    private void loadJson(String json){
        
        this.json = new Gson().fromJson(json, Map.class);
       
        setAdapters();
        //setReceivers();
        Adapters adapters = new Adapters();
        
        System.out.println(adapters);
    }

    private void setAdapters() {
        
        ((ArrayList<Object>) this.json.get("subrules")).stream().forEach((item) -> {
            ((ArrayList<Object>)((LinkedTreeMap<String,Object>) item).get("actions")).stream().forEach((item2) -> {
                Adapters adapters = new Adapters();
                String target = (String) ((LinkedTreeMap<String,Object>) ((LinkedTreeMap<String,Object>)item2).get("target")).get("topic");
                String topic = "/SM" + target;
                String adapter = target.substring(1).replace("/+", "/all").replace('/', '_');
                adapters.newAdapter("target", topic, adapter);
                ((ArrayList<Object>)((LinkedTreeMap<String,Object>) ((LinkedTreeMap<String,Object>) ((LinkedTreeMap<String,Object>)item2).get("function")).get("listen_data")).get("listeners")).stream().forEach((item3) -> {
                    Adapters adp = new Adapters();
                    String receiver = (String) ((LinkedTreeMap<String,Object>) item3).get("topic");
                    Pattern tpc = Pattern.compile("/[^/]+" + receiver.replace("/+", "/[^/]+"));
                    String adr = receiver.substring(1).replace("/+", "/all").replace('/', '_');
                    adp.newAdapter("receiver", tpc, adr);
                    adp.newEntry(adr, topic);
                    
                });
            });
        });
    }
    
    /*private void setReceivers() {

        ((ArrayList<Object>) this.json.get("subrules")).stream().forEach((item) -> {
            ((ArrayList<Object>)((LinkedTreeMap<String,Object>) item).get("actions")).stream().forEach((item2) -> {
                ((ArrayList<Object>)((LinkedTreeMap<String,Object>) ((LinkedTreeMap<String,Object>) ((LinkedTreeMap<String,Object>)item2).get("function")).get("listen_data")).get("listeners")).stream().forEach((item3) -> {
                    Adapters adapters = new Adapters();
                    String target = (String) ((LinkedTreeMap<String,Object>) item3).get("topic");
                    Pattern topic = Pattern.compile("/[^/]+" + target.replace("/+", "/[^/]+"));
                    String adapter = target.substring(1).replace("/+", "/all").replace('/', '_');
                    adapters.newAdapter("receiver", topic, adapter);
                });
            });
        });
    }*/
}