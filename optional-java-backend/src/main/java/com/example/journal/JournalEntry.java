package com.example.journal;

import java.util.List;

public class JournalEntry {
    private String date;
    private String mood;
    private List<String> tags;
    private String text;

    // No-arg constructor for JSON deserialization
    public JournalEntry() {}

    // getters + setters
    public String getDate(){ return date; }
    public void setDate(String d){ this.date=d; }
    public String getMood(){ return mood; }
    public void setMood(String m){ this.mood=m; }
    public List<String> getTags(){ return tags; }
    public void setTags(List<String> t){ this.tags=t; }
    public String getText(){ return text; }
    public void setText(String t){ this.text=t; }
}
