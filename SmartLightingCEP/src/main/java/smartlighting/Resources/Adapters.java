/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.Resources;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *
 * @author bernardo
 */
public class Adapters {
    private static Map<String, List<String>> adapters = new HashMap<>();
    
    public List<String> getAdapters(String key){
        return adapters.get(key);
    }
    
    public void newAdapter(String key, String value){
        if(adapters.containsKey(key)){
            adapters.get(key).add(value);
        }
        else{
            List<String> list = new ArrayList<>();
            list.add(value);
            adapters.put(key, list);
        }
    }
}
 