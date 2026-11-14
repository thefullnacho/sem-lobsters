/* LOCAL PATCH of Brinkmann's multi_alphadeficit.c: 128-bit sets, up to 127 vertices. Not for redistribution. */

/*
ONLY for trees. It is tested in the beginning whether the graph read is a tree!

An alpha - labelling of a graph with n vertices is a labelling with values
1,2,...,n so that there is a number k with 1<k<=n so that each edge is adjacent
with a value in 1..(k-1) and a value in k..n. The label of an edge is the absolute 
value of the difference of the labels of its two vertices. The set of possible
labels is 1..n-1. The error of a labelling is the number of possible edge labels that
do not occur. So in case of error 0 all possible edge labels 1..n-1 occur. 

The alpha deficiency is the smallest error over all possible alpha-labellings.

We choose the number k to be the kardinality of the bipartition set containing vertex 1.
A labelling where vertex 1 gets a larger number can be transformed into one of the
constructed form by assigning to every vertex i the label |V|+1-label(i).

If a parameter is given, the parameter is treated as a name and graphs with positive 
alphadeficit are written to a file with this name -- UNLESS:

If the parameter starts with a minus then it must be followed by an f and the rest is
interpreted as a number so that graphs with this alpha deficit must be written to stdout
-- e.g. -f3 -- meaning filter out graphs with alpha deficit 3

10 augustus 2009: inserted something that uses the fact that if a labelling with a certain 
deficit is given, then you get another labelling with the same deficit if you reverse 
the labels inside both of the classes 1...limit and (limit+1)...|V|. To this end we require
that the vertex labelled one is smaller than the vertex labelled limit.

A lot of the code would benefit from some cleaning up. Former ways to do things needed "repetition"
of the code because a lot of parameters had to be changed. After some changes, it would be possible
to use just one part of the code instead (see e.g. dolabel() and dolabel_0()). But maybe the danger
of inserting errors is bigger than the possible advantage...


*/

#include<stdio.h>
#include<stdlib.h>
#include<memory.h>
#include<limits.h>

#define leer 255 
#define VERTICES 127 // local patch: 128 bit sets (unsigned __int128), vertex numbers start at 1 
                    // and the vertex numbers start at 1
#define MARK_LIMIT (USHRT_MAX-2)
#define ENDLIST INT_MAX // to mark the end of a list of vertices

typedef int GRAPH[VERTICES+1][VERTICES+1];
typedef int ADJAZENZ[VERTICES+1];
typedef unsigned __int128 ULLI; // local patch, was unsigned long long

#define BIT(i) ((((ULLI) 1)<<(i)))
#define NBIT(i) (~(BIT(i)))

#define ABSMIN(a,b) (((a)<(b))?((b)-(a)):((a)-(b)))

// de volgende variabelen waren vroeger parameters maar om efficientieredenen is het beter
// ze globaal te hebben en niet altijd te kopieren
int *listend;
GRAPH graph;
ADJAZENZ adj;
ULLI class1=0, class2=0; // de twee bipartitieklassen als bitmaps
int limit; // de toppen in class1 worden 1...limit gelabelled
int lijst[VERTICES+1]; // de BFS lijst van toppen met ENDLIST het laatste element 
int voorganger[VERTICES+1]; // voorganger[i] is de (unieke) top die een buur is van i en voor i in
                            // de lijst staat. Voor de eerste top in de lijst is dat INT_MAX
int label[VERTICES+1]={0}, invlabel[VERTICES+1]={0};
char possibility[VERTICES+1][VERTICES+1][2]; // the list of possibilities. posibility[i][j] is the j-th possibility
// to assign label i. The entry [0] gives the value of class 1 that must be used (1..limit) and the value of [1] the 
// value of class 2 (limit+1..n).
int volgorde[VERTICES+1]={0}; // the order of vertices so that edges around these vertices are tried
int inv_volgorde[VERTICES+1]={0}; 
int maxdeg;

int _marks[VERTICES+1];
int _mark=INT_MAX;
#define RESETMARKS { int _i; \
                  if (_mark==INT_MAX) \
                     { for (_i=0;_i<=VERTICES;_i++)  _marks[_i]=0;\
                       _mark=1; }\
                  else _mark++; }
#define ISMARKED(i) (_marks[i] ==_mark)
#define IS_UNMARKED(i) (_marks[i] !=_mark)
#define MARK(i) (_marks[i] =_mark)
#define UNMARK(i) (_marks[i] = 0)

int _reachmarks[VERTICES+1];
int _reachmark=INT_MAX;
#define RESETREACHMARKS { int _i; \
                  if (_reachmark==INT_MAX) \
                     { for (_i=0;_i<=VERTICES;_i++)  _reachmarks[_i]=0;\
                       _reachmark=1; }\
                  else _reachmark++; }
#define ISREACHMARKED(i) (_reachmarks[i] == _reachmark)
#define IS_REACHUNMARKED(i) (_reachmarks[i] != _reachmark)
#define REACHMARK(i) (_reachmarks[i] =_reachmark)
#define REACHUNMARK(i) (_reachmarks[i] = 0)



void writeset(ULLI set)
{
  int i;

  fprintf(stderr,"-------------------------------------\nThe set: \n");
  for (i=0;i<128;i++) if (set & BIT(i)) fprintf(stderr,"%d ",i);
  fprintf(stderr,"\n-------------------------------------\n");

}


void schreibegraph(GRAPH g, ADJAZENZ adj)

{
 int x,y, unten,oben, maxvalence;
fprintf(stderr,"\n\n ");

for(x=1, maxvalence=0; x <= g[0][0]; x++) if (adj[x]>maxvalence) maxvalence=adj[x];

fprintf(stderr,"|%2d",g[0][0]);

for(x=1; (x <= g[0][0])&&(x<=24); x++)  fprintf(stderr,"|%2d",x); fprintf(stderr,"|\n");

fprintf(stderr," ");

for(x=0; (x <= g[0][0])&&(x<=24); x++) fprintf(stderr,"|==");    fprintf(stderr,"|\n");

for(x=0; x < maxvalence; x++)
  {
   fprintf(stderr," |  ");
   for(y=1; (y<=g[0][0])&&(y<=24); y++)
       if ((g[y][x] ==leer) || (x>=adj[y])) fprintf(stderr,"|  "); else fprintf(stderr,"|%2d",g[y][x]);
       fprintf(stderr,"|\n");
  }

unten=25; oben=48;

while(g[0][0]>=unten)
{
fprintf(stderr,"\n");

fprintf(stderr,"    ");

for(x=unten; (x <= g[0][0])&&(x<=oben); x++)  fprintf(stderr,"|%2d",x); fprintf(stderr,"|\n");

fprintf(stderr,"    ");

for(x=unten; (x <= g[0][0])&&(x<=oben); x++) fprintf(stderr,"|==");    fprintf(stderr,"|\n");

for(y=0; y < maxvalence; y++)
  {
   fprintf(stderr,"    ");
   for(x=unten; (x <= g[0][0])&&(x<=oben); x++)
       if ((g[x][y]==leer) || (y>=adj[x])) fprintf(stderr,"|  "); else fprintf(stderr,"|%2d",g[x][y]);
       fprintf(stderr,"|\n");
  }
unten += 24; oben += 24; 
}

}





void einfugen (GRAPH graph,ADJAZENZ adj,int v, int w)
/* Fuegt die Kante (v,w) in den Graphen graph ein. Dabei wird aber davon */
/* ausgegangen, dass in adj die wirklich aktuellen werte fuer die */
/* Adjazenzen stehen. Die adjazenzen werden dann aktualisiert. */

{
graph[v][adj[v]]=w;
graph[w][adj[w]]=v;
adj[v]++;
adj[w]++;
}


void decodiere(unsigned char  *code,GRAPH graph,ADJAZENZ adj,int codelaenge)

{
int i,j;
int vertexnumber;
GRAPH localgraph;

/* adj[] wird passend belegt UND jede liste graph[i] wird mit "leer" abgeschlossen ". */

// decoding with the localgraph buffer and afterwards reversing the order of the neighbours
// is especially for the code produced by ruskey_to_mult from the output of Frank
// Ruskeys tree generator. The labellings have a lot of structure and are not "random" --
// with this reversed order the tests are much faster (about 40% for maxdeg 3 23 vertices)


graph[0][0]=vertexnumber=code[0];
graph[0][1]=codelaenge-vertexnumber;

 if (vertexnumber>VERTICES) { fprintf(stderr,"Not prepared for so many vertices\n"); exit(1); }

for (i=1; i<= vertexnumber; i++) adj[i]=0; 

j=1;

for (i=1; i<codelaenge; i++) 
            { if (code[i]==0) j++; else einfugen(localgraph,adj,j,code[i]); }
for (i=1; i<= vertexnumber; i++) for (j=adj[i]-1;j>=0;j--) graph[i][adj[i]-1-j]=localgraph[i][j];
for (i=1; i<= vertexnumber; i++) graph[i][adj[i]]=0;
}


/****************************LESE_MULTICODE************************/

int lese_multicode(unsigned char**code, int *codelaenge, FILE *fil)

/* Liest den code und gibt EOF zurueck, wenn das Ende der Datei erreicht
   ist, 1 sonst. Der Speicher fuer den code wird alloziert, falls noetig,
   was entschieden wird anhand der lokalen Variablen maxknotenzahl */
{
static int maxknotenzahl= -1;
int codel, gepuffert=0;
int vertexnumber,a,b,nuller;
unsigned char ucharpuffer;

if ((vertexnumber=getc(fil))==EOF) return EOF;
if (vertexnumber==0) { fprintf(stderr,"Umschaltung auf short noch nicht implementiert.\n");
                     exit(0);
                    } 
nuller=0; codel=1;
if (vertexnumber=='>') /* koennte ein header sein -- oder 'ne 62, also ausreichend fuer
			     unsigned char */
      { gepuffert=1;
	a=getc(fil);
	if(a==0) nuller++; 
	b=getc(fil);
	if(b==0) nuller++; 
	/* jetzt wurden 3 Zeichen gelesen */
	if ((a=='>') && (b=='m')) /*garantiert header*/
	  { 
	    gepuffert=0;
	    while ((ucharpuffer=getc(fil)) != '<');
	    /* noch zweimal: */ ucharpuffer=getc(fil); 
	    if (ucharpuffer!='<') { fprintf(stderr,"Problems with header -- single '<'\n"); exit(1); }
	    if ((vertexnumber=getc(fil))==EOF) return EOF;
	    /* kein graph drin */
	  }
	/* else kein header */
      }


if (vertexnumber > maxknotenzahl)
  { if (*code) free(*code);
    *code=(unsigned char *)malloc((vertexnumber*(vertexnumber-1)/2+vertexnumber)*sizeof(unsigned char));
    if (code==NULL) { fprintf(stderr,"Do not get memory for code\n"); exit(0); }
    maxknotenzahl=vertexnumber;
  }

(*code)[0]=vertexnumber; if (gepuffert) { codel=3; (*code)[1]=a; (*code)[2]=b; }

while (nuller<vertexnumber-1)
  { if (((*code)[codel]=getc(fil))==0) nuller++;
    codel++; }

*codelaenge=codel;
return 1;
}

void getmaxdeg_klassen_testcon(GRAPH graph,ADJAZENZ adj,int *maxdeg,
			       ULLI *class1, ULLI *class2, 
			       int *limit,int lijst[],int voorganger[])
     // in lijst wordt een BFS-volgorde beginnend met top 1 teruggegeven
{
  int top,i,j,run,end;

  if (graph[0][0]-1 != graph[0][1])
      { fprintf(stderr,"Input graph not a tree %d vertices, %d edges -- exiting.\n",
		graph[0][0],graph[0][1]); 
        exit(0); }


  (*class1) = BIT(1);
  (*class2) = 0;
  *limit=1;
  MARK(1);
  lijst[0]=1;
  voorganger[1]=INT_MAX;
  *maxdeg=adj[1];

  for (run=end=0; run<=end; run++)
    {
      top= lijst[run];
      if (adj[top]>(*maxdeg)) (*maxdeg)=adj[top];
      // het volgende gebruikt dat de graaf bipartiet is -- maar als het geen boom is
      // wordt toch al afgebroken
      if (BIT(top) & (*class1)) // alles in class2 stoppen
	{ 
	  for (i=0;i<adj[top];i++)
	    { j=graph[top][i];
	    if (!(BIT(j) & (*class2))) // nog niet bezocht
	      { (*class2) |= BIT(j);
	        end++; lijst[end]=j;
		voorganger[j]=top;
	      }
	    }
	}
      else // alles in class1 stoppen
	{
	  for (i=0;i<adj[top];i++)
	    { j=graph[top][i];
	    if (!(BIT(j) & (*class1))) // nog niet bezocht
	      { (*class1) |= BIT(j);
	        (*limit)++;
	        end++; lijst[end]=j;
		voorganger[j]=top;
	      }
	    }
	}
    }

  if ((end+1) != graph[0][0])
       { fprintf(stderr,"Input graph not a tree -- not connected!\n");
        exit(0); }

  return;
}

//int heuristic(GRAPH graph,ADJAZENZ adj, ULLI class1, 
//	      ULLI class2, int limit)
/* returns a simple upper bound for the alpha deficit. Vertices are just
   labelled greedily. Depending on the performance maybe later a better heuristic
   can be used -- tests must show whether that can help. */
//{
  //long long int visited=0, used=0;

  // LATER

//}

int stupid_lookahead(int *lijst, GRAPH graph,ADJAZENZ adj, ULLI class1, 
		     ULLI class2, int limit, 
		     ULLI present, int label[], ULLI assigned)
// kijkt gewoon aan hoeveel toppen al geen waarde meer toegekend kan worden zonder
// de error te verhogen
{

  int forced_error, top, ok,i,j,l,x;
  int stop=0; 
  // als een top zonder gelabelde buur wordt gevonden heeft de rest ook geen gelabelde buren

  // de lijst is in breadth first volgorde en bovendien is het een boom. Elke top heeft dus ten hoogste
  // 1 al gelabelde buur

  for (forced_error=0; (!stop) && ((top=*lijst) != ENDLIST); lijst++)
    {
      for (j=0;(j<adj[top]) && !(l=label[graph[top][j]]);j++);
      if (j==adj[top]) {stop=1;}
      else
	{
	  ok=0;
	  if ((BIT(top) & class1))
	    {
	      for (i=1;(i<=limit) && !ok;i++)
		if (!(assigned & BIT(i)))
		    { x = ABSMIN(l,i); // het nieuwe label
		    if (!(BIT(x) & present)) ok=1;
		    }
	    }
	  else // top zit in class2
	    {
	      for (i=limit+1;i<=graph[0][0];i++)
		if (!(assigned & BIT(i)))
		    { x = ABSMIN(l,i); // het nieuwe label
		    if (!(BIT(x) & present)) ok=1;
		    }
	    }
	  if (!ok) forced_error++;
	}
    }

  return forced_error;

}

void stupid_verder(int *lijst, int error_so_far,
		  int *best_error, ULLI present, 
		  ULLI assigned)
{
  int errorbuffer, i, j, l, x, top, ok;

// de lijst is in breadth first volgorde en bovendien is het een boom. Elke top hier heeft dus 
// precies 1 al gelabelde buur


  if (*best_error==0) return;
  top=*lijst;
  if (top==ENDLIST) { *best_error=error_so_far; return; }

  if (*best_error==1) // dan moeten de kleinste en de grootste waarde buren zijn om het te verbeteren
    { 
      if ((i=invlabel[1]))
	{ 
	  if ((l=invlabel[graph[0][0]])) // dan moeten ze buren zijn
	    { 
	    for (j=ok=0;!ok && (j<adj[i]);j++) if (graph[i][j]==l) ok=1;
	    }
	  else // dan moet er een buur zonder label zijn
	    { 
	    for (j=ok=0;!ok && (j<adj[i]);j++) if (label[graph[i][j]]==0) ok=1;
	    }
	  if (!ok) return;
	}
      else
	if ((i=invlabel[graph[0][0]]))// maar 1 niet assigned
	  {
	    for (j=ok=0;!ok && (j<adj[i]);j++) if (label[graph[i][j]]==0) ok=1;
	    if (!ok) return;
	  }
    }


  //i=stupid_lookahead(lijst,graph,adj,class1, class2, limit, present, label, assigned);
  // vertraging om factor 2
  //if (i+error_so_far >= (*best_error)) return; // kan niet meer beter worden dan best-so-far


  l=label[voorganger[top]];

  if ((BIT(top) & class1))
    {
      for (i=1;i<=limit;i++)
	if (!(assigned & BIT(i)))
	  {
	    x = ABSMIN(l,i); // het nieuwe label
	    if (BIT(x) & present) errorbuffer=error_so_far+1;
	    else errorbuffer=error_so_far;

	    if (errorbuffer< (*best_error))
	      {
		label[top]=i; invlabel[i]=top;
		stupid_verder(lijst+1,errorbuffer, 
			      best_error, present | BIT(x), assigned | BIT(i));
		label[top]=0; invlabel[i]=0;
	      }
	  }
    }
  else // top zit in class2
    {
      //for (i=limit+1;i<=graph[0][0];i++)
      for (i=graph[0][0];i>limit;i--) // deze volgorde voor 16, maxdeg 3 bijna 20 keer sneller
	if (!(assigned & BIT(i)))
	  {
	    x = ABSMIN(l,i); // het nieuwe label
	    if (BIT(x) & present) errorbuffer=error_so_far+1;
	    else errorbuffer=error_so_far;

	    if (errorbuffer< (*best_error))
	      {
		label[top]=i; invlabel[i]=top;
		stupid_verder(lijst+1,errorbuffer, 
			      best_error, present | BIT(x), assigned | BIT(i));
		label[top]=0; invlabel[i]=0;
	      }
	  }
    }

  return;

}


int stupid_straight(int lijst[])
/* een stomme straightforward manier om de alpha-deficit te berekenen -- vooral bedoeld
   om een onafhankelijke test voor de andere routine te hebben die op kleine
   grafen toegepast kan worden. Probeert min of meer alle permutaties van
   labels in de klassen */

{
  ULLI present=0; // which edge-labels are already present
  int error_so_far; // How many edge labels are already non-unique
  int best_error=INT_MAX;
  ULLI assigned=0; // which vertex labels are already assigned
  int i,top,testvalue;


  //schreibegraph(graph,adj); writeset(class1); writeset(class2); fprintf(stderr,"---\n\n\n");

  top=lijst[0];

  if (!(BIT(top) & class1)) { fprintf(stderr,"The first vertex in the list should be in class 1...\n"); 
                            exit(1); }
  lijst[graph[0][0]]=ENDLIST;
  listend=lijst+graph[0][0];

  // het wordt eerst geprobeerd labellings te vinden met lage error -- de meeste bomen hebben
  // die en daardoor kan beter gesnoeid worden. Voorbeeld 16 toppen maxdeg 3: iets meer dan
  // 3 keer sneller zo

  for (testvalue=1; testvalue>0; testvalue++) 
    // testvalue doet alsof een labelling met error 1 groter dan gezocht wordt al gevonden is
    {
      error_so_far=0;
      best_error=testvalue;
      for (i=1;i<=limit;i++)
	{
          label[top]=i; invlabel[i]=top;
	  assigned |= BIT(i);
	  stupid_verder(lijst+1, 0, &best_error, present, assigned);
          assigned = 0; invlabel[i]=0;
	}
      if (best_error<testvalue) testvalue= -1;
    }

  return best_error;
}


void prepare()
// make the list of edges and assign the classes to the vertices
{
  int locallijst[VERTICES+1], *run, *end, top, top2, i, j; // voor de BFS
  int degreelist[VERTICES+1][VERTICES+1], aantaldeg[VERTICES+1]={0}, deg;

  if (graph[0][1]!=graph[0][0]-1) { fprintf(stderr,"Not a tree -- exiting\n"); exit(1); }
  maxdeg=0;

  locallijst[0]=1; 
  class1 = BIT(1);
  class2=0;
  run=locallijst; end=locallijst+1;
  limit=1;

  for (;run<end;run++)
    {
      top= *run;
      deg=adj[top];
      if (deg> maxdeg) maxdeg=deg;
      degreelist[deg][aantaldeg[deg]]=top;
      aantaldeg[deg]++;
      if (class1 & BIT(top))
	{
	  for (i=0; i<adj[top]; i++)
	    { top2=graph[top][i];
	      if (!(class2 & BIT(top2)))
		{
		  class2 |= BIT(top2);
		  *end=top2; end++;
		}
	    }
	}
      else // dus top in class 2
	{
	  for (i=0; i<adj[top]; i++)
	    { top2=graph[top][i];
	      if (!(class1 & BIT(top2)))
		{ limit++;
		  class1 |= BIT(top2);
		  *end=top2; end++;
		}
	    }
	}
    }

  if (end-locallijst != graph[0][0]) { fprintf(stderr,"Graph not connected -- exiting!\n");
                                       exit(1); }

  for (i=1, run=volgorde;i<=maxdeg;i++) // vertices with low degree come earlier in volgorde
    // this is also used in the dolabel-routines to judge which vertex has degree one
  //for (i=maxdeg, run=volgorde;i>0;i--) tried this one and it is worse! (factor about 2-3) 
    { 
      for(j=aantaldeg[i]-1;j>=0;j--) 
	// for the graphs of Frank Ruskeys tree generator it is important to have them in this reverse order
	// otherwise the test takes much more time
	{ *run=degreelist[i][j]; run++; }
    }
    for (i=0;i<graph[0][0];i++) inv_volgorde[volgorde[i]]=i;

  return;
}

int extra_doublelabel(int top,int vlabel, ULLI *edgelabels_used, ULLI forbiddenlabels)
// returns the extra deficit that is produced by assigning label to top.
// edgelabels_used is updated with the new edgelabels that are produced this way.
// in case a forbidden label occurs the number of vertices is returned -- a value sure reject the labelling 
{
  int j,vlabel2,edgelabel,extradef,top2;

  extradef=0;
  for (j=0; (top2=graph[top][j]); j++)
    { 
      if ((vlabel2=label[top2]))
	{ edgelabel=ABSMIN(vlabel2,vlabel);
	  if (BIT(edgelabel) & forbiddenlabels) return graph[0][0];
	  if (BIT(edgelabel) & (*edgelabels_used)) { extradef++; }
	  else *edgelabels_used |= BIT(edgelabel);
	}
    }
  return extradef;
}



int dolabel_finish(int *labellist, ULLI edgelabels_used, ULLI vertexlabels_used, int maxdeficit, int doublelabels, 
	    int missinglabels, ULLI forbiddenlabels)
// returns 1 if a labelling has been found with deficit maxdeficit or smaller
// the same as dolabel -- only without testing invlabel[1]<invlabel[limit]

{
  int elabel, vlabel1, vlabel2, i, j, k, top, top2, extradoublelabel, doublelabelbuffer, deg_one_done, buffer;
  int for_top1, for_top2;
  ULLI edgelabels_used_buffer, edgelabels_used_buffer2;
  char forbidden[VERTICES+1];

  //fprintf(stderr,"New call edgelabel %d -- doubles=%d\n",*labellist,doublelabels);
  //for (i=1; i<=graph[0][0]; i++) fprintf(stderr,"l[%d]=%d  ",i,label[i]);
  //fprintf(stderr,"\n");

  // this routine may be called also for other edge labels than n-1 and 1 if they are missing
 
  elabel=*labellist;

  while (BIT(elabel)& edgelabels_used)
    { labellist++;  elabel=*labellist; } // search for next label to assign

  if (elabel==0) return 1; 
  // all edge labels are assigned (or not) with deficit at most maxdeficit. Maybe not all vertex labels are assigned, but
  // assigning the remaining vertex labels randomly can only decrease the deficit. In fact I would be astonished
  // if the case of not all vertex labels assigned could ever occur... Edge labels would have to be forbidden...


  for (i=0; possibility[elabel][i][0]!=0; i++) 
// here the possibility number i is tried. The possibility of NOT using this edge label at all is tested afterwards
    { vlabel1=possibility[elabel][i][0]; vlabel2=possibility[elabel][i][1];
      if (vertexlabels_used & BIT(vlabel1))
	{ 
	  if (vertexlabels_used & BIT(vlabel2)) {}
	  /* bad luck -- both labels used but the edgelabel not yet given -- so not much can be done */
	  else 
	    // so vlabel1 exists and the vertex is of course in class 1. vlabel2 does not yet exist
	    { top=invlabel[vlabel1];
	      deg_one_done=0;
	      for (j=0;(top2=graph[top][j]);j++)
		{ 
		  if (!(label[top2]) && (!deg_one_done || (adj[top2]>1))) 
		    { if (adj[top2]==1) deg_one_done=1; // all other deg 1 vertices adjacent to top1 that still
		      // can be labelled are equivalent to this one
		      edgelabels_used_buffer2=edgelabels_used;
		      extradoublelabel= extra_doublelabel(top2,vlabel2,&edgelabels_used_buffer2,forbiddenlabels);
		      if (doublelabels+extradoublelabel <= maxdeficit)
			{
			  label[top2]=vlabel2; invlabel[vlabel2]=top2;
			  if (dolabel_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
				      vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
				      maxdeficit, doublelabels+extradoublelabel,
				      missinglabels,forbiddenlabels)) return 1;
			  label[top2]=0; invlabel[vlabel2]=0;
			}
		    }
		} // end for
	    }// end else

	}
      else
	{
	  if (vertexlabels_used & BIT(vlabel2)) 
	    // vlabel2 used, vlabel1 NOT used and the vertex with vlabel2 is of course in class2
	    { 
	      top=invlabel[vlabel2];
	      deg_one_done=0;
	      for (j=0;(top2=graph[top][j]);j++)
		{ 
		      if (!(label[top2])&& (!deg_one_done || (adj[top2]>1))) // make sure you didn't see the edge before
			{ if (adj[top2]==1) deg_one_done=1; 
			  edgelabels_used_buffer2=edgelabels_used;
			  extradoublelabel= extra_doublelabel(top2,vlabel1,&edgelabels_used_buffer2,forbiddenlabels);
			  if (doublelabels+extradoublelabel <= maxdeficit)
			    if (doublelabels+extradoublelabel <= maxdeficit)
			      {
				label[top2]=vlabel1; invlabel[vlabel1]=top2;
				if (dolabel_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					    vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
					    maxdeficit, doublelabels+extradoublelabel,
					    missinglabels,forbiddenlabels)) return 1;
				label[top2]=0; invlabel[vlabel1]=0;
			      }
			}
		} // end for
	    }
	  else // none of the labels already used
	    { for (k=graph[0][0];k ;k--) forbidden[k]=0;
	      for (k=0; k< graph[0][0]; k++)
		{ 
		  top=volgorde[k];  
		  if (!(label[top]) && !(forbidden[top]))
		    {
		      if (adj[top]==1) // forbid all other edges from degree 1 vertices neighbouring top2
			{ top2=graph[top][0];
			  for (j=0; (buffer=graph[top2][j]); j++)
			    if (adj[buffer]==1) { forbidden[buffer]=1; }
			}

		      if (BIT(top) & class1) // top is in class 1 
			{ for_top1=vlabel1; for_top2=vlabel2; }
		      else
			{ for_top1=vlabel2; for_top2=vlabel1; }
		      edgelabels_used_buffer=edgelabels_used;
		      extradoublelabel= extra_doublelabel(top,for_top1,&edgelabels_used_buffer,forbiddenlabels);
		      if (doublelabels+extradoublelabel <= maxdeficit)
			{ doublelabelbuffer=doublelabels+extradoublelabel;
			  label[top]=for_top1; invlabel[for_top1]=top;
			  for (j=0;(top2=graph[top][j]);j++)
			    if (!(label[top2]) && (inv_volgorde[top2]>k)) 
			      // each edge labelled from the first vertex in volgorde
			      {
				edgelabels_used_buffer2=edgelabels_used_buffer;
				extradoublelabel= extra_doublelabel(top2,for_top2,&edgelabels_used_buffer2,forbiddenlabels);
				if (doublelabelbuffer+extradoublelabel <= maxdeficit)
				  {
				    label[top2]=for_top2; invlabel[for_top2]=top2;
				    if (dolabel_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
						vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
						maxdeficit, doublelabelbuffer+extradoublelabel,
						missinglabels,forbiddenlabels)) return 1;
				    label[top2]=0; invlabel[for_top2]=0;
				  }
			      } // end for () if ()
			  label[top]=0; invlabel[for_top1]=0;
			}// end first extra doublelabel not too large
		    } // end top not labelled and not forbidden
		} // end for alle toppen
	    }// end else -- case none of the labels already used
	} // end else -- vlabel1 not used
    } // end for over all possibilities
      if (missinglabels<maxdeficit)
	{
	  if (dolabel_finish(labellist+1, edgelabels_used, vertexlabels_used,  maxdeficit, doublelabels,
		      missinglabels+1, forbiddenlabels | BIT(elabel))) return 1;
	}

  return 0;

}




int dolabel(int *labellist, ULLI edgelabels_used, ULLI vertexlabels_used, int maxdeficit, int doublelabels, 
	    int missinglabels, ULLI forbiddenlabels)
// returns 1 if a labelling has been found with deficit maxdeficit or smaller


{
  int elabel, vlabel1, vlabel2, i, j, k, top, top2, extradoublelabel, doublelabelbuffer, deg_one_done, buffer;
  int for_top1, for_top2;
  ULLI edgelabels_used_buffer, edgelabels_used_buffer2;
  char forbidden[VERTICES+1];

  //fprintf(stderr,"New call edgelabel %d -- doubles=%d\n",*labellist,doublelabels);
  //for (i=1; i<=graph[0][0]; i++) fprintf(stderr,"l[%d]=%d  ",i,label[i]);
  //fprintf(stderr,"\n");

  // this routine may be called also for other edge labels than n-1 and 1 if they are missing
 
  if (invlabel[1] && invlabel[limit])
    {
      // here it happens exactly after two steps -- these labels are always assigned after the first two edge labels
      if (invlabel[1]<invlabel[limit]) return 0;
      else return dolabel_finish(labellist, edgelabels_used, vertexlabels_used, maxdeficit, doublelabels, 
				 missinglabels, forbiddenlabels);
    }

  elabel=*labellist;

  while (BIT(elabel)& edgelabels_used)
    { labellist++;  elabel=*labellist; } // search for next label to assign

  if (elabel==0) return 1; 
  // all edge labels are assigned (or not) with deficit at most maxdeficit. Maybe not all vertex labels are assigned, but
  // assigning the remaining vertex labels randomly can only decrease the deficit. In fact I would be astonished
  // if the case of not all vertex labels assigned could ever occur... Edge labels would have to be forbidden...


  for (i=0; possibility[elabel][i][0]!=0; i++) 
// here the possibility number i is tried. The possibility of NOT using this edge label at all is tested afterwards
    { vlabel1=possibility[elabel][i][0]; vlabel2=possibility[elabel][i][1];
      if (vertexlabels_used & BIT(vlabel1))
	{ 
	  if (vertexlabels_used & BIT(vlabel2)) {}
	  /* bad luck -- both labels used but the edgelabel not yet given -- so not much can be done */
	  else 
	    // so vlabel1 exists and the vertex is of course in class 1. vlabel2 does not yet exist
	    { top=invlabel[vlabel1];
	      deg_one_done=0;
	      for (j=0;(top2=graph[top][j]);j++)
		{ 
		  if (!(label[top2]) && (!deg_one_done || (adj[top2]>1))) 
		    { if (adj[top2]==1) deg_one_done=1; // all other deg 1 vertices adjacent to top1 that still
		      // can be labelled are equivalent to this one
		      edgelabels_used_buffer2=edgelabels_used;
		      extradoublelabel= extra_doublelabel(top2,vlabel2,&edgelabels_used_buffer2,forbiddenlabels);
		      if (doublelabels+extradoublelabel <= maxdeficit)
			{
			  label[top2]=vlabel2; invlabel[vlabel2]=top2;
			  if (dolabel(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
				      vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
				      maxdeficit, doublelabels+extradoublelabel,
				      missinglabels,forbiddenlabels)) return 1;
			  label[top2]=0; invlabel[vlabel2]=0;
			}
		    }
		} // end for
	    }// end else

	}
      else
	{
	  if (vertexlabels_used & BIT(vlabel2)) 
	    // vlabel2 used, vlabel1 NOT used and the vertex with vlabel2 is of course in class2
	    { 
	      top=invlabel[vlabel2];
	      deg_one_done=0;
	      for (j=0;(top2=graph[top][j]);j++)
		{ 
		      if (!(label[top2])&& (!deg_one_done || (adj[top2]>1))) // make sure you didn't see the edge before
			{ if (adj[top2]==1) deg_one_done=1; 
			  edgelabels_used_buffer2=edgelabels_used;
			  extradoublelabel= extra_doublelabel(top2,vlabel1,&edgelabels_used_buffer2,forbiddenlabels);
			  if (doublelabels+extradoublelabel <= maxdeficit)
			    if (doublelabels+extradoublelabel <= maxdeficit)
			      {
				label[top2]=vlabel1; invlabel[vlabel1]=top2;
				if (dolabel(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					    vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
					    maxdeficit, doublelabels+extradoublelabel,
					    missinglabels,forbiddenlabels)) return 1;
				label[top2]=0; invlabel[vlabel1]=0;
			      }
			}
		} // end for
	    }
	  else // none of the labels already used
	    { for (k=graph[0][0];k ;k--) forbidden[k]=0;
	      for (k=0; k< graph[0][0]; k++)
		{ 
		  top=volgorde[k];  
		  if (!(label[top]) && !(forbidden[top]))
		    {
		      if (adj[top]==1) // forbid all other edges from degree 1 vertices neighbouring top2
			{ top2=graph[top][0];
			  for (j=0; (buffer=graph[top2][j]); j++)
			    if (adj[buffer]==1) { forbidden[buffer]=1; }
			}

		      if (BIT(top) & class1) // top is in class 1 
			{ for_top1=vlabel1; for_top2=vlabel2; }
		      else
			{ for_top1=vlabel2; for_top2=vlabel1; }
		      edgelabels_used_buffer=edgelabels_used;
		      extradoublelabel= extra_doublelabel(top,for_top1,&edgelabels_used_buffer,forbiddenlabels);
		      if (doublelabels+extradoublelabel <= maxdeficit)
			{ doublelabelbuffer=doublelabels+extradoublelabel;
			  label[top]=for_top1; invlabel[for_top1]=top;
			  for (j=0;(top2=graph[top][j]);j++)
			    if (!(label[top2]) && (inv_volgorde[top2]>k)) 
			      // each edge labelled from the first vertex in volgorde
			      {
				edgelabels_used_buffer2=edgelabels_used_buffer;
				extradoublelabel= extra_doublelabel(top2,for_top2,&edgelabels_used_buffer2,forbiddenlabels);
				if (doublelabelbuffer+extradoublelabel <= maxdeficit)
				  {
				    label[top2]=for_top2; invlabel[for_top2]=top2;
				    if (dolabel(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
						vertexlabels_used | BIT(vlabel1) | BIT(vlabel2),
						maxdeficit, doublelabelbuffer+extradoublelabel,
						missinglabels,forbiddenlabels)) return 1;
				    label[top2]=0; invlabel[for_top2]=0;
				  }
			      } // end for () if ()
			  label[top]=0; invlabel[for_top1]=0;
			}// end first extra doublelabel not too large
		    } // end top not labelled and not forbidden
		} // end for alle toppen
	    }// end else -- case none of the labels already used
	} // end else -- vlabel1 not used
    } // end for over all possibilities
      if (missinglabels<maxdeficit)
	{
	  if (dolabel(labellist+1, edgelabels_used, vertexlabels_used,  maxdeficit, doublelabels,
		      missinglabels+1, forbiddenlabels | BIT(elabel))) return 1;
	}

  return 0;

}



int no_doublelabel(int top,int vlabel, ULLI *edgelabels_used)
// returns 0 if a double label is produced -- 1 else
// edgelabels_used is updated

{
  int j,vlabel2,edgelabel,top2;

  for (j=0; (top2=graph[top][j]); j++)
    { 
      if ((vlabel2=label[top2]))
	{ edgelabel=ABSMIN(vlabel2,vlabel);
	  if (BIT(edgelabel) & (*edgelabels_used)) return 0;
	  else *edgelabels_used |= BIT(edgelabel);
	}
    }
  return 1;
}

int dolabel_0_finish(int *labellist, ULLI edgelabels_used, ULLI vertexlabels_used)
// returns 1 if a labelling has been found with deficit 0
// identiek aan dolabel_0 -- alleen dat niet meer getest wordt of invlabel[1]<invlabel[limit]


{
  int elabel, vlabel1, vlabel2, i, j, k, top, top2, deg_one_done, buffer;
  ULLI edgelabels_used_buffer, edgelabels_used_buffer2;
  char forbidden[VERTICES+1];

  //fprintf(stderr,"New call edgelabel %d -- doubles=%d\n",*labellist,doublelabels);
  //for (i=1; i<=graph[0][0]; i++) fprintf(stderr,"l[%d]=%d  ",i,label[i]);
  //fprintf(stderr,"\n");

  elabel=*labellist;

  while (BIT(elabel)& edgelabels_used)
    { labellist++;  elabel=*labellist; } // search for next label to assign

  if (elabel==0) return 1; 
  // all edge labels are assigned (or not) with deficit at most maxdeficit. Maybe not all vertex labels are assigned, but
  // assigning the remaining vertex labels randomly can only decrease the deficit. In fact I would be astonished
  // if the case of not all vertex labels assigned could ever occur... Edge labels would have to be forbidden...


  for (i=0; (vlabel1=possibility[elabel][i][0])!=0; i++) 
// here the possibility number i is tried. 
    { 
      vlabel2=possibility[elabel][i][1];
      if (vertexlabels_used & BIT(vlabel1))
	{
	  if (vertexlabels_used & BIT(vlabel2)) {}
	  /* bad luck -- both labels used but the edgelabel not yet given -- so not much can be done */
	  else 
	    // so vlabel1 exists and the vertex is of course in class 1. vlabel2 does not yet exist
	    { top=invlabel[vlabel1];
	      deg_one_done=0;
	      for (j=0; (top2=graph[top][j]);j++)
		{ 
		  if (!(label[top2]) && (!deg_one_done || (adj[top2]>1))) 
		    { if (adj[top2]==1) deg_one_done=1; // all other deg 1 vertices adjacent to top1 that still
		      // can be labelled are equivalent to this one
		      edgelabels_used_buffer2=edgelabels_used;
		      if (no_doublelabel(top2,vlabel2,&edgelabels_used_buffer2)) 
			{
			  label[top2]=vlabel2; invlabel[vlabel2]=top2;
			  if (dolabel_0_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
			  label[top2]=0; invlabel[vlabel2]=0;
			}
		    }
		} // end for
	    }// end else

	}
      else
	{
	  if (vertexlabels_used & BIT(vlabel2)) // vlabel2 used, vlabel1 NOT used and the vertex with vlabel2 is of course in class2
	    {
	      top=invlabel[vlabel2];
	      deg_one_done=0;
	      for (j=0; (top2=graph[top][j]);j++)
		{ 
		      if (!(label[top2]) && (!deg_one_done || (adj[top2]>1))) // make sure you didn't see the edge before
			{ if (adj[top2]==1) deg_one_done=1; // all other deg 1 vertices adjacent to top1 that still
		          // can be labelled are equivalent to this one
			  edgelabels_used_buffer2=edgelabels_used;
			  if (no_doublelabel(top2,vlabel1,&edgelabels_used_buffer2))
			    {
			      label[top2]=vlabel1; invlabel[vlabel1]=top2;
			      if (dolabel_0_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					    vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
			      label[top2]=0; invlabel[vlabel1]=0;
			    }
			}
		} // end for
	    }
	  else // none of the labels already used
	    { for (k=graph[0][0];k ;k--) forbidden[k]=0;
	      for (k=0; k< graph[0][0]; k++)
		{
		  top=volgorde[k];  
		  if (!(label[top]) && !(forbidden[top]))
		    {
		      if (adj[top]==1) // forbid all other edges from degree 1 vertices neighbouring top2
			{ top2=graph[top][0];
			  for (j=0; (buffer=graph[top2][j]); j++)
			    if (adj[buffer]==1) { forbidden[buffer]=1; }
			}

		      if (BIT(top) & class1)
			{ edgelabels_used_buffer=edgelabels_used;
			  if (no_doublelabel(top,vlabel1,&edgelabels_used_buffer))
			    { 
			      label[top]=vlabel1; invlabel[vlabel1]=top;
			  for (j=0;(top2=graph[top][j]);j++)
			    if (!(label[top2]) && (inv_volgorde[top2]>k))
			      { 			  
				edgelabels_used_buffer2=edgelabels_used_buffer;
				if (no_doublelabel(top2,vlabel2,&edgelabels_used_buffer2))
				  {
				    label[top2]=vlabel2; invlabel[vlabel2]=top2;
				    if (dolabel_0_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
							 vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
				    label[top2]=0; invlabel[vlabel2]=0;
				  }
			      } // end for () if
			  label[top]=0; invlabel[vlabel1]=0;
			    }// end first extra doublelabel not too large
			}// end top in class 1
		      else // top in class 2
			{ edgelabels_used_buffer=edgelabels_used;
			  if (no_doublelabel(top,vlabel2,&edgelabels_used_buffer))
			    { 
			      label[top]=vlabel2; invlabel[vlabel2]=top;
			      for (j=0;(top2=graph[top][j]);j++)
				if (!(label[top2]) && (inv_volgorde[top2]>k))
				  {
				    edgelabels_used_buffer2=edgelabels_used_buffer;
				    if (no_doublelabel(top2,vlabel1,&edgelabels_used_buffer2))
				      {
					label[top2]=vlabel1; invlabel[vlabel1]=top2;
					if (dolabel_0_finish(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
							     vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
					label[top2]=0; invlabel[vlabel1]=0;
				      }
				  } // end for () if
			      label[top]=0; invlabel[vlabel2]=0;
			    }// end first extra doublelabel not too large
			}// end top in class 2
		    } // end if not labelled and not forbidden
		}// end for over all vertices
	    }// end else -- case none of the labels already used
	} // end else -- vlabel1 not used
    } // end for over all possibilities

  return 0;

}


int dolabel_0(int *labellist, ULLI edgelabels_used, ULLI vertexlabels_used)
// returns 1 if a labelling has been found with deficit 0


{
  int elabel, vlabel1, vlabel2, i, j, k, top, top2, buffer;
  ULLI edgelabels_used_buffer, edgelabels_used_buffer2;
  char forbidden[VERTICES+1]={0}; 
			     // forbidden[i]!=0 means don't test edges starting at i because and equivalent edge has
			     // already been tested. In fact this is only applied for edges where vertex i has
			     // degree one -- others always have forbidde[i]=0 

  //fprintf(stderr,"New call edgelabel %d -- doubles=%d\n",*labellist,doublelabels);
  //for (i=1; i<=graph[0][0]; i++) fprintf(stderr,"l[%d]=%d  ",i,label[i]);
  //fprintf(stderr,"\n");

  if (invlabel[1] && invlabel[limit])
    {
      // here it happens exactly after two steps -- these labels are always assigned after the first two edge labels
      if (invlabel[1]<invlabel[limit]) return 0;
      else return dolabel_0_finish(labellist, edgelabels_used, vertexlabels_used);
    }

  elabel=*labellist; // here that is always not assigned

  if (elabel==0) return 1; 
  // all edge labels are assigned (or not) with deficit at most maxdeficit. Maybe not all vertex labels are assigned, but
  // assigning the remaining vertex labels randomly can only decrease the deficit. In fact I would be astonished
  // if the case of not all vertex labels assigned could ever occur... Edge labels would have to be forbidden...


  vlabel1=possibility[elabel][0][0]; // only one possibility here
  vlabel2=possibility[elabel][0][1];

  // none of the vertex labels already used because for edge labels n-1 and 1 the vertex labels can only
  // overlap for stars -- and that is caught in the alpha_deficit routine 

  for (k=0; k< graph[0][0]; k++)
    {
      top=volgorde[k];
      if (!(label[top]) && !forbidden[top])
	{
	  if (adj[top]==1) // forbid all other edges from degree 1 vertices neighbouring top2
	    { top2=graph[top][0];
	      for (i=0; (buffer=graph[top2][i]); i++)
		if (adj[buffer]==1) { forbidden[buffer]=1; }
	    }
	  // the degree one vertices come first in volgorde, so edges are seen first from the degree one vertices
	  if (BIT(top) & class1)
	    { edgelabels_used_buffer=edgelabels_used;
	      if (no_doublelabel(top,vlabel1,&edgelabels_used_buffer))
		{ 
		  label[top]=vlabel1; invlabel[vlabel1]=top;
		  for (j=0;(top2=graph[top][j]);j++)
		    if (inv_volgorde[top2]>k // each edge is labelled from the first occurence in volgorde
		        && !(label[top2])) 
			{			  
			  edgelabels_used_buffer2=edgelabels_used_buffer;
			  if (no_doublelabel(top2,vlabel2,&edgelabels_used_buffer2))
			    {
			      label[top2]=vlabel2; invlabel[vlabel2]=top2;
			      if (dolabel_0(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					    vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
			      label[top2]=0; invlabel[vlabel2]=0;
			    }
		    } // end for() if
		  label[top]=0; invlabel[vlabel1]=0;
		}// end first extra doublelabel not too large
	    } // end top in class 1
	  else // top in class 2
	    { edgelabels_used_buffer=edgelabels_used;
	      if (no_doublelabel(top,vlabel2,&edgelabels_used_buffer))
		{ 
		  label[top]=vlabel2; invlabel[vlabel2]=top;
		  for (j=0;(top2=graph[top][j]);j++)
		    if (inv_volgorde[top2]>k // each edge is labelled from the first occurence in volgorde
		        && !(label[top2])) 
			{
			  edgelabels_used_buffer2=edgelabels_used_buffer;
			  if (no_doublelabel(top2,vlabel1,&edgelabels_used_buffer2))
			    {
			      label[top2]=vlabel1; invlabel[vlabel1]=top2;
			      if (dolabel_0(labellist+1, edgelabels_used_buffer2 | BIT(elabel), 
					    vertexlabels_used | BIT(vlabel1) | BIT(vlabel2))) return 1;
			      label[top2]=0; invlabel[vlabel1]=0;
			    }
		    } // end for
		  label[top]=0; invlabel[vlabel2]=0;
		}// end first extra doublelabel not too large
	    } // end top in class 2

	} // end not labelled and not forbidden
    } // end for over all vertices

  return 0;

}





int alpha_deficit()
/* returns the alpha deficit of the graph stored in the global variable graph. It starts to find
   a labelling with deficit 0 first. Most graphs have it and it allows better bounding criteria.
   If that isn't found it starts to search for deficit 1, then deficit 2, etc. 

   The general algorithm is to branch over the labellings of edges and trying to assign the label to
   all edges and by using all possible vertex labels.

   First the edge labels with a small number of possibilities for vertex labels are tried -- 
   (n-1) and 1 have only 1 possibility for labels. Then n-2 and 2, etc
*/

{
  int maxdeficit, *listp, i, j, start; 
  ULLI edgelabels_used, vertexlabels_used;
  static int oldg00= -1; // remembers the value of graph[0][0] to decide whether labellist must be changed
  static int oldlimit= -1;
  static int labellist[VERTICES+1];

  prepare();
  if ((limit==1) || (limit== graph[0][0]-1)) 
    // the star is treated separately because this is the only case where the edges labelled n-1 and 1 can share an edge
    {
      oldg00=oldlimit= -1; return 0;
    }

  if (graph[0][0]!=oldg00)
    { 
      if (graph[0][0]%2)
	{ for (i=1, listp=labellist; i<=(graph[0][0]-1)/2; i++)
	    { 
	      *listp = i; listp++;
	      *listp = graph[0][0]-i; listp++;
	    }
	}
      else
	{ for (i=1, listp=labellist; i<=graph[0][0]/2; i++)
	    { 
	      *listp = i; listp++;
	      *listp = graph[0][0]-i; listp++;
	    }
	  *listp = i; listp++;
	}
      *listp = 0; // marks the end

    }


  // Now fill in all the possibilities to label edges with value k. What is possible depends on
  // the value of "limit"

  if ((graph[0][0]!=oldg00) || (oldlimit != limit))
    {
      for (i=graph[0][0]-1; i>0; i--)
	{ j=0;
	  if (graph[0][0]-i>limit) start=limit+i; else start=graph[0][0];
	  for ( ; (start>limit) && (start-i>0); start--)
	    { possibility[i][j][0]=start-i; possibility[i][j][1]=start; j++; }
	  possibility[i][j][0]=possibility[i][j][1]=0;

	  { // another ordering seems to work better...
#define WISSEL(a,b) { buffer=(a)[0]; (a)[0]=(b)[0]; b[0]=buffer; buffer=(a)[1]; (a)[1]=(b)[1]; b[1]=buffer; }
	    int buffer, start, end;
	    start=0; end=(j/2);
	    while (start<end) { WISSEL(possibility[i][start],possibility[i][end]) start++; end--; }
#undef WISSEL

	  }
	  
	}
    }
    
  oldg00=graph[0][0]; oldlimit=limit;

  edgelabels_used= vertexlabels_used= 0;
  for (i=graph[0][0]; i>0; i--) label[i]=invlabel[i]=0;

  if (dolabel_0(labellist, edgelabels_used, vertexlabels_used)) return 0; 
  // that's a special version that does most of the work and uses deficit 0

  for (maxdeficit=1; 1; maxdeficit++)
    {
      if (dolabel(labellist, edgelabels_used, vertexlabels_used, maxdeficit, 0, 0, 0)) return maxdeficit;
    }

  return INT_MAX; // can never be reached -- just to make sure the compiler doesn't complain

}



/******************************MAIN**********************************/

int main(int argc,char *argv[])

{

  int zaehlen=0, i,j, codelaenge, filtervalue= -1;
unsigned char *code=NULL;
int alphadef_list[VERTICES+1][VERTICES+1]={{0}};
// the number of graphs with maxdeg [i] and alpha deficit j is in alphadef[i][j]
int alphadef;
FILE *fil=NULL;
char *filename=NULL;

 srand(0);

 if (sizeof(ULLI)!=16) 
   { fprintf(stderr,"Sorry -- expected 64 bit unsigned long long int -- exiting\n");
     exit(1); }

 for (i=1; i<argc; i++)
   {if (argv[i][0]=='-')
       { if (argv[i][1]!='f') { fprintf(stderr,"Wrong options -- read program header\n"); exit(1); }
	 i++; filtervalue=atoi(argv[i]);
       }
     else filename=argv[i];
   }
    
while(lese_multicode(&code, &codelaenge, stdin) != EOF)
  {
    zaehlen++; 
    decodiere(code,graph,adj,codelaenge); 
    //fprintf(stderr,"Graph Nr. %d\n",zaehlen); schreibegraph(graph,adj); 
    //getmaxdeg_klassen_testcon(graph,adj,&maxdeg, &class1, &class2, &limit, lijst, voorganger);
    //alphadef=heuristic(graph,adj,class1, class2, limit);
    //alphadef=stupid_straight(lijst);

    //schreibegraph(graph,adj); 

    alphadef= alpha_deficit();
    if (alphadef==filtervalue) { fwrite(code,1,codelaenge,stdout); fflush(stdout); }
    if (alphadef && filename) 
      {
	if (fil==NULL) 
	  { fil=fopen(filename,"w");
	    if (fil==NULL) 
	      { fprintf(stderr,"Can't open file %s for writing -- exiting.\n",filename);
		exit(1); }
	  }
	    fwrite(code,1,codelaenge,fil);
      }

    //fprintf(stderr,"maxdeg %d alphadef %d\n",maxdeg, alphadef);
    (alphadef_list[maxdeg][alphadef])++;
  }

 for (i=1;i<VERTICES;i++) 
   for (j=0;j<VERTICES;j++)
     if (alphadef_list[i][j]) fprintf(stderr,"Graphs with maxdeg %d and alpha-deficit %d: %d\n",
				      i,j,alphadef_list[i][j]);

 if (fil != NULL) fclose(fil);

return(0);

}



