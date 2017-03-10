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
public class Targets {
    private List<Pair<String, String>> targets = new ArrayList();
    
    public void addTarget(String queryTopic, String topic){
    
        Pair<String, String> target = new Pair<>(queryTopic, topic);
        targets.add(target);
    }
    
    public List<Pair<String, String>> getTargets(){
        return targets;
    }
}
