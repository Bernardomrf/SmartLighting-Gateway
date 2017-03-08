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
import javafx.util.Pair;

/**
 *
 * @author bernardo
 */
public class Adapters {
    private static Map<String, List<Pair<Object, String>>> adapters = new HashMap<>();
    
    public List<Object> getAdapters(String key){
        List<Object> tmp = new ArrayList<>();
        adapters.get(key).stream().forEach((i) -> {
            tmp.add(i.getKey());
        });
        return tmp;
    }
    
    public void newAdapter(String type, Object regex, String adapter){
        if(adapters.containsKey(type)){
            adapters.get(type).add(new Pair(regex, adapter));
        }
        else{
            List<Pair<Object, String>> list = new ArrayList<>();
            list.add(new Pair(regex, adapter));
            adapters.put(type, list);
        }
    }
}
 