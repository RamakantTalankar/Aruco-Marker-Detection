#include<stdio.h>
#include<stdlib.h>
#include<string.h>
// # include "grammarDef.h"
# define NT 6
# define T 6
# define no_of_lines 9

typedef struct grammarNode{
    int isTerminal; 
    struct grammarNode* next; 
    struct grammarNode* prev;
    char* name;
}node; 

node* grammar[no_of_lines];

int follow[NT][T+1]={0}; //the last terminal is $
int first[NT][T]={0};
char* terminal[T];
int ind_eps=T-1;  // index of psilon is last
char* non_terminal[NT];

int checkTerminal(char* name)
{
    if(name[0] - 'a' >=0)
    {
        if('z' - name[0] < 26)
        {
            return 1; 
        }
    } 

    return 0; 
}

void grammarInitialize(FILE* fp)
{ 
    char buf[100];
    int lineno = 0;
    while(fgets(buf, sizeof(buf) , fp))
    {
        char* token = strtok(buf," "); 
        node* curr = (node*)malloc(sizeof(node)); 
        curr->name = (char*)malloc(sizeof(char)*strlen(token));
        strcpy(curr->name, token);
        curr -> isTerminal = checkTerminal(token); 
        curr -> next = NULL; 
        curr -> prev = NULL; 
        grammar[lineno] = curr;
       
        // printf("%s ", curr -> name); 
        token = strtok(NULL, " ");
        while(token != NULL)
        {
            node* temp = (node*)malloc(sizeof(node)); 
            temp->name = (char*)malloc(sizeof(char)*strlen(token));
            strcpy(temp->name ,token);
            // printf("%s ", temp -> name);
            temp -> isTerminal = checkTerminal(token);
            temp -> next = NULL; 
            temp -> prev = curr; 
            curr -> next = temp; 
            curr = curr -> next; 
            token = strtok(NULL, " "); 
        }
        // printf("1");
    //  printf("\n");
        lineno++; 
    } 
    fclose(fp);
}

int checkeps(char* name)   //check if the string is e
{
    for(int i = 0; i<no_of_lines; i++)
    {
        if(strcmp(grammar[i]->name, name) == 0)
        {
            node* temp = malloc(sizeof(node)); 
            temp = grammar[i]->next; 
            if(strcmp(temp->name, "epsilon") == 0)
            {
                return 1; 
            } 
            else 
            {
                return 0; 
            }
        }
    }
}

int find_index_t(char* name)
{
    for(int i = 0; i<T; i++)
    {
        if(*(terminal[i]) == *(name))
        {
            return i; 
        }
    } 
}

int find_index_nt(char* name)
{
    for(int i = 0; i<NT; i++)
    {
        if(*(non_terminal[i])== *(name))
        {
            return i; 
        }
    } 
}

// //make array for grammar and initialize globally here.
// void fill_terminal()
// {
//     //populate terminal array. file input output
// }

// void fill_non_terminal()
// {
//     //populate nt array from file.
//     //populate nt array from file.
// }

void fill2(int i,  int a)
{
    for(int k=0;k<=T;k++)
    {
        if(follow[a][k]==1)
            follow[i][k]=1;
    }
}

void fill1(int i,  int a)
{
    for(int j=0;j<T-1;j++)
    { 
        if(first[a][j]==1)
            follow[i][j]=1;
    }
}
int z=0;
int first_contains_epsilon(int a)
{
    return first[a][T-1];// we have assumed that epsilon is the last symnol at index T-1 in the first table as well as terminal array.
}
void follow1(int i,int *check)
{
    
    // char *c1=non_terminal[i];
    if(check[i]==0)
    {
        for(int j=0;j<no_of_lines;j++)
        {
            node* p=grammar[j];
            p=p->next;
            while(p!=NULL)
            {
                // printf("%d",z++);
                // printf("%s \n",non_terminal[i]);

                // for(int h=0;h<non_terminal)
                if(*(p->name) == *(non_terminal[i]))
                {
                    // printf("1  \n");
                    if(p->next==NULL)
                    {
                        int a=find_index_nt(grammar[j]->name);
                        if(!check[a] && i!=a)
                            follow1(a,check);
                        fill2(i,a);
                        break;
                    }

                    else if(p->next!=NULL && (p->next)->isTerminal==1)
                    {
                        int b=find_index_t((p->next)->name);//mark in follow that follow(p) is p->next->name; 
                        follow[i][b]=1;
                        break;
                    }
                    else if(p->next!=NULL && (p->next)->isTerminal==0)
                    {
                        // printf("1");
                        while((p->next)!=NULL)
                        {
                            int a= find_index_nt((p->next)->name);
                            // if(i==1) printf("%d",a);
                            fill1(i,a); //fill everything except epsilon at initial time
                            if(first_contains_epsilon(a))  //now if the first contains epsilon move to next non terminal in rule
                            {
                                
                                p=p->next;
                            }
                            else  //esle your job is done simply break
                            {
                                p=p->next;
                                break;
                            }
                        }
                        if(p->next==NULL)
                        {
                            int a=find_index_nt(grammar[j]->name);

                            if(!check[a] && i!=a)
                                follow1(a,check);
                            fill2(i,a);
                            break;
                        }
                    }  
                }

                else
                {
                    p=p->next;
                }
            }
        }

        check[i]=1;
        // printf("%d",i);   
     }
            
       

}

void print_gr()
{
    for(int i = 0; i < no_of_lines; i++)
    {
        node* curr = grammar[i]; 
        while(curr != NULL)
        {
            printf("%s ", curr->name); 
            curr = curr -> next; 
        }
       
    }
}

void follow_set()
{
    
    int check1[NT]={0};
    
   
    follow[0][T]=1;  //Follow of start is $
    check1[0]=1;
    
    for(int i=1;i<NT;i++)
    {
    //    printf("hi");
        follow1(i,check1);
    }

        
}
     

int main()
{
    terminal[0]="id";
    terminal[1]="ii";
    terminal[2]="mm";
    terminal[4]="bo";
    terminal[3]="bc";
    terminal[5]="epsilon";

    non_terminal[0]="PP";
    non_terminal[1]="EE";
    non_terminal[2]="XX";
    non_terminal[3]="TT";
    non_terminal[4]="YY";
    non_terminal[5]="FF";

   

    first[0][0]=1;
    first[0][4]=1;
    first[1][0]=1;
    first[1][4]=1;
    first[2][1]=1;
    first[2][5]=1;
    first[3][0]=1;
    first[3][4]=1;
    first[4][2]=1;
    first[4][5]=1;
    first[5][0]=1;
    first[5][4]=1;

     

    FILE* fp = fopen("testcase.txt","r");
    // printf("1");
    grammarInitialize(fp);
    // printf("hello\n");

    // print_gr();
   follow_set();

   

    for(int i=0;i<NT;i++)
    {
        for(int j=0;j<=T;j++)
        {
            printf("%d ",follow[i][j]);
        }
        printf("\n");
    }

    return 0;
}


