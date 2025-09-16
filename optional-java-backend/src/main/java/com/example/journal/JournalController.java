package com.example.journal;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import java.util.Map;
import java.util.*;

@RestController
@RequestMapping("/api/entries")
@CrossOrigin // Allow requests from frontend (adjust origins as needed)
public class JournalController {
    private final List<JournalEntry> store = Collections.synchronizedList(new ArrayList<>());

    @PostMapping
    public ResponseEntity<String> receiveEntry(@RequestBody Map<String, Object> entry) {
        // For debugging: print the entry to the console
        System.out.println("Received entry: " + entry);
        // TODO: Save entry to database or file if needed
        return new ResponseEntity<>("Entry received", HttpStatus.OK);
    }

    @GetMapping
    public List<JournalEntry> list(){
        return store;
    }
}
