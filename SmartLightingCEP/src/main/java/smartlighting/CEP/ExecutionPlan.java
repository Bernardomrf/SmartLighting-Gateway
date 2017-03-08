/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.CEP;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import redis.clients.jedis.Jedis;
import smartlighting.Resources.Adapters;

/**
 *
 * @author bernardo
 */
public class ExecutionPlan {
    
    private String ep;
    private Map<String, Object> json;
    private Adapters redis;
    
    public ExecutionPlan(String ep, String json){
        loadJson(json);
        loadEP(ep);
        
    }
    
    private void loadEP(String ep){
        this.ep = ep;
    }
    
    private void loadJson(String json){
        
        this.json = new Gson().fromJson(json, Map.class);
       
        setTargets();
        //String topic = ((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(1)).get("actions")).get(0)).get("target")).get("topic"));
        //System.out.println(((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(0)).get("actions")).get(0)).get("target")).get("topic")));
        //System.out.println(((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(1)).get("actions")).get(0)).get("target")).get("topic")));
        
    }

    private void setTargets() {
        String target;
        for (Object item : ((ArrayList<Object>) this.json.get("subrules"))) {
            Adapters adapters = new Adapters();
            adapters.newAdapter("in", ((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>)((LinkedTreeMap<String,Object>) item).get("actions")).get(0)).get("target")).get("topic")));
        }
    }
    
    private void setReceivers() {
        String target;
        for (Object item : ((ArrayList<Object>) this.json.get("subrules"))) {
            Adapters adapters = new Adapters();
            adapters.newAdapter("in", ((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>)((LinkedTreeMap<String,Object>) item).get("actions")).get(0)).get("target")).get("topic")));
        }
    }
}
