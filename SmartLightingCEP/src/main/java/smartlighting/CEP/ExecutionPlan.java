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

/**
 *
 * @author bernardo
 */
public class ExecutionPlan {
    
    private String ep;
    private Map<String, Object> json;
    
    public ExecutionPlan(){
    
    }
    
    public void loadEP(String ep){
        
    }
    
    public void loadJson(String json){
        this.json = new Gson().fromJson(json, Map.class);
        
        //String topic = ((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(1)).get("actions")).get(0)).get("target")).get("topic"));
        System.out.println(((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(0)).get("actions")).get(0)).get("target")).get("topic")));
        System.out.println(((String) ((LinkedTreeMap<String,Object>)((LinkedTreeMap<String,Object>) ((ArrayList<Object>) ((LinkedTreeMap<String,Object>) ((ArrayList<Object>) this.json.get("subrules")).get(1)).get("actions")).get(0)).get("target")).get("topic")));
        
    }
}
