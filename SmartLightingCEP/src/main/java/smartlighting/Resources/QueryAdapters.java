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
public class QueryAdapters {
    private static Map<String, Pair<Listeners, Targets>> queryAdapters= new HashMap<>();
    
    public void setQueryAdapters(String query, Listeners listener, Targets targets){
        Pair<Listeners, Targets> adapters = new Pair<>(listener, targets);
        queryAdapters.put(query, adapters);
    }
    
    public Map<String, Pair<Listeners, Targets>> getQueryAdapters(){
    
        return queryAdapters;
    }
    
    public List<Listeners> getAllListeners(){
    
        List<Listeners> listeners = new ArrayList();
        
        queryAdapters.keySet().stream().forEach((query) -> {
            listeners.add(queryAdapters.get(query).getKey());
        });
        
        return listeners;
    }
    
    public Listeners getListeners(String query){
        return queryAdapters.get(query).getKey();
    }
    
    public Targets getTargets(String query){
    
        return queryAdapters.get(query).getValue();
    }
    
    
    
}
