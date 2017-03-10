/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.Resources;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import javafx.util.Pair;

/**
 *
 * @author bernardo
 */
public class Listeners {
    private List<Pair<Pattern, String>> listeners = new ArrayList();
    
    public void setListener(Pattern regex, String topic){
        Pair<Pattern, String> pair = new Pair<>(regex, topic);
        listeners.add(pair);
    }
    
    public List<Pair<Pattern, String>> getListeners(){
        
        return listeners;
    }
}
