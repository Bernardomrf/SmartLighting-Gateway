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
    private static HashMap<String, List<String>> relations = new HashMap<>();
    
    public List<Pair<Object, String>> getAdapters(String key){
        List<Pair<Object, String>> tmp = new ArrayList<>();
        adapters.get(key).stream().forEach((i) -> {
            Pair<Object, String> pair = new Pair<Object, String>(i.getKey(), i.getValue());
            tmp.add(pair);
        });
        return tmp;
    }
    
    public List<String> getRelations(String key){
        return relations.get(key);
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
    
    public void newEntry(String in_event, String out_event){
        if(relations.containsKey(in_event)){
            relations.get(in_event).add(out_event);
        }
        else{
            ArrayList<String> new_list = new ArrayList<>();
            new_list.add(out_event);
            relations.put(in_event, new_list);
        }
    }
}
 