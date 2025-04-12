import java.util.ArrayList;





class StartUp{
    int size;
    int hits=0;
    boolean stateGame= false;
    String[] ar = new String[2];
    ArrayList<String> loc = new ArrayList<>();
    public void setLocation(ArrayList<String> e){
        
        loc = e;
    }
    public String checkLocation(String x){
        String responce= "MISS";
        for(String c:ar){
            if (x.equals(c)){
                responce = "HIT";
                hits++;
            }
            if(hits==2){
                responce="KILL";
            }
        }
        return responce;
    }
}

public class tester{
    public static void main(String[] args){
        //first startup
        StartUp amazon = new StartUp();
        ArrayList<String> locations0= new ArrayList<>();
        String x= "A6";
        String y= "A8";
        String z= "A7";
        locations0.add(x);
        locations0.add(y);
        locations0.add(z);
        amazon.setLocation(locations0);



        //Second startup
        StartUp google = new StartUp();
        ArrayList<String> locations1= new ArrayList<>();
        String a= "A6";
        String b= "A8";
        String c= "A7";
        locations1.add(a);
        locations1.add(b);
        locations1.add(c);
        google.setLocation(locations1);




        //Third startup
        StartUp facebook = new StartUp();
        ArrayList<String> locations2= new ArrayList<>();
        String d= "A6";
        String e= "A8";
        String f= "A7";
        locations2.add(d);
        locations2.add(e);
        locations2.add(f);
        facebook.setLocation(locations2);

        
       
        System.out.println("Input first guess");
        String input = "A6";
        String result = google.checkLocation(input);
        System.out.println(result);
        System.out.println(google.hits);
        if (result == "KILL"){
            System.out.println("YOU WON");
    }

}
}
