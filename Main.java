package com.company;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Main {

    public static void main(String args[]) throws IOException {

        //Loading an existing document
        File file = new File("Colonization-of-the-Internet.pdf");
        PDDocument document = PDDocument.load(file);

        //Instantiate PDFTextStripper class
        PDFTextStripper pdfStripper = new PDFTextStripper();
        pdfStripper.setParagraphStart("\t");
        pdfStripper.setSortByPosition(true);

        //Retrieving text from PDF document
        String text = pdfStripper.getText(document);

        text = text.replaceAll("\\.", "xyzxyz").toLowerCase();
        text = text.replaceAll("!", "xyzxyz").toLowerCase();


        // replace all non alphabetic characters
        text = text.replaceAll("\\p{Punct}", "").toLowerCase();
        text = text.replaceAll("\\[\\d+\\]", "").toLowerCase();

        // removing stop words
        File stopwords = new File("stopWords.txt");
        Scanner myReader = new Scanner(stopwords);

        while (myReader.hasNextLine()) {
            String stopword = myReader.nextLine();
            text = text.replaceAll(" "+stopword+" "," ");
        }
        myReader.close();


        // splitting into paragraphs
        String[] paras = text.split("\t");
        List<String> list = new ArrayList<String>();
        for(int k = 0; k < paras.length; k++){
            paras[k] = paras[k].replace("\r\n"," ");
            String[] words = paras[k].split(" ");
            if (words.length > 6){
                if (words[0].length()>0 && !Character.isDigit(words[0].charAt(0))){
                        list.add(paras[k]);
                }
            }
        }
        paras =  list.toArray(new String[ list.size() ]);
        list = new ArrayList<String>();
        for(int k = 0; k < paras.length; ){
            paras[k] = paras[k].replace("\r\n"," ");
            String[] words = paras[k].split(" ");
            if (words.length > 6){
                if (words[0].length()>0 && !Character.isDigit(words[0].charAt(0))){
                    if (!words[words.length-1].contains("xyzxyz")) {
                        String concat = paras[k];
                        while (true){
                            k++;
                            if (k == paras.length){
                                break;
                            }
                            paras[k] = paras[k].replace("\r\n"," ");
                            String[] new_words = paras[k].split(" ");
                            concat =  concat + " " + paras[k];
                            if (new_words[new_words.length-1].contains("xyzxyz")){
                                k++;
                                break;
                            }
                        }
                        list.add(concat);

                    }
                    else {
                        list.add(paras[k]);
                        k++;
                    }
                }
                else{
                    k++;
                }
            }
            else{
                k++;
            }

        }
        paras =  list.toArray(new String[ list.size() ]);

        // creating trie and assigning paragraph number to nodes
        Node root = new Node(' ');
        Node current = root;
        Node next;
        //iterate through paragraphs
        for(int k = 0; k < paras.length; k++)
        {
            paras[k] = paras[k].replace("\r\n"," ");
            paras[k] = paras[k].replace("xyzxyz","");
            String[] words = paras[k].split(" ");
            //iterate through words in paragraph k
            for (int i = 0; i < words.length; i++)
            {
                String word = words[i];
                current = root;
                // iterate through characters of each word
                for (int j = 0; j < word.length(); j++)
                {
                    char letter = word.charAt(j);
                    next = current.getChild(letter);

                    //if child is not found then create and add child
                    if (next == null) {
                        Node child = new Node(letter);
                        current.addChild(child);
                        current = child;
                    }
                    // go to next child
                    else
                        current = next;
                }
                current.addParagraph(k);
            }
        }
        // input query from user to search
        System.out.println("Enter query to search or -1 to exit:");
        Scanner in = new Scanner(System.in);

        while (true) {
            String query = in.nextLine();
            query = query.toLowerCase();
            if(query.equals("-1"))
                break;

            String[] lookups = query.split(" ");

            List<Integer> result = new ArrayList<>();

            // for query containing more than 2 words
            if (lookups.length > 3) {
                String keyword1 = lookups[0];
                String keyword2 = lookups[2].substring(1);
                String keyword3 = lookups[4].substring(0, lookups[4].length() - 1);

                if (lookups[3].equals("and")) {
                    result = intersectionList(getParas(keyword2, root), getParas(keyword3, root));
                    if (lookups[1].equals("and")) {
                        result = intersectionList(getParas(keyword1, root), result);
                    } else if (lookups[1].equals("or")) {
                        result = unionList(getParas(keyword1, root), result);
                    }
                } else if (lookups[3].equals("or")) {
                    result = unionList(getParas(keyword2, root), getParas(keyword3, root));
                    if (lookups[1].equals("and")) {
                        result = intersectionList(getParas(keyword1, root), result);
                    } else if (lookups[1].equals("or")) {
                        result = unionList(getParas(keyword1, root), result);
                    }
                    else
                        System.out.println("Invalid query syntax");

                }

            // query with 2 words
            } else if (lookups.length > 1) {
                String keyword1 = lookups[0];
                String keyword2 = lookups[2];

                if (lookups[1].equals("and")) {
                    result = intersectionList(getParas(keyword1, root), getParas(keyword2, root));
                } else if (lookups[1].equals("or")) {
                    result = unionList(getParas(keyword1, root), getParas(keyword2, root));
                }
                else
                    System.out.println("Invalid query syntax");

            }
            // single word query
            else {
                result = getParas(query, root);
            }

            if (result.size() > 0) {
                System.out.println("Success");
                System.out.println("The word(s) are in the following paragraphs");
                printList(result);
            } else
                System.out.println("Failure! No match found\n");
        }
        //Closing the document
        document.close();

    }

    //function to get paragraph list from the word lookup
    public static List<Integer> getParas(String lookup, Node root)
    {
        Node current = root;
        for(int i = 0; i < lookup.length(); i++)
        {
            current = current.getChild(lookup.charAt(i));
            if (current == null)
            {
                List<Integer> empty = new ArrayList<>();
                return empty;
            }
        }
        return current.getParagraphs();
    }

    //returns intersection of 2 lists
    public static List<Integer> intersectionList(List<Integer> list1, List<Integer> list2)
    {
        boolean found;
        List<Integer> inter = new ArrayList<>();
        for(int i = 0; i < list1.size(); i++)
        {
            if (list2.contains(list1.get(i)))
                inter.add(list1.get(i));
        }
        return inter;
    }

    // returns union of 2 lists
    public static List<Integer> unionList(List<Integer> list1, List<Integer> list2)
    {
        List<Integer> union = new ArrayList<>();

        for(int i = 0; i < list1.size(); i++)
            union.add(list1.get(i));

        for(int i = 0; i < list2.size(); i++)
        {
            if (!list1.contains(list2.get(i)))
                union.add(list2.get(i));
        }
        return union;
    }

    //print elements of list
    public static void printList(List<Integer> list)
    {
        for(int i = 0; i < list.size(); i++)
        {
            System.out.print(" " + list.get(i) + " ");
        }
        System.out.println("\n");
    }

}
