extern crate rand;
extern crate gnuplot;
extern crate dataplotlib;

use dataplotlib::util::{linspace};
use gnuplot::{Figure, Caption, Color};
use std::io::{BufReader,BufRead};
use std::fs::File;
use std::collections::HashMap;
use rand::Rng;

// read a graph from file and return its adjacency list
fn read_graph(file: String) -> HashMap<i32,Vec<i32>>{
    let mut graph = HashMap::new();
    let f = File::open(file).unwrap();
    let file = BufReader::new(&f);
    for line in file.lines() {
        let l = line.unwrap();
        let ch = l.chars().next().unwrap();
        if ch != '#' {
            let mut edges = l.split("\t");
            let ug = edges.next().unwrap();
            let vg = edges.next().unwrap();
            let u: i32 = ug.parse().unwrap();
            let v: i32 = vg.parse().unwrap();
            if v != u {
                graph.entry(u).or_insert(Vec::new()).push(v);
                graph.entry(u).or_insert(Vec::new()).sort();
                graph.entry(u).or_insert(Vec::new()).dedup();
                graph.entry(v).or_insert(Vec::new()).push(u);
                graph.entry(v).or_insert(Vec::new()).sort();
                graph.entry(v).or_insert(Vec::new()).dedup();
            }
        }
    }
    return graph;
}

// generate a random graph with n nodes and that for each
// couple of nodes there is p probability to find an edge
fn er(n: i32,p:f64)->HashMap<i32,Vec<i32>>{
    let mut graph: HashMap<i32,Vec<i32>> = HashMap::new();
    for u in 0..n{
        // graph.insert(u,Vec::new());
        for v in 0..n{
            if v != u {
                let a: f64 = rand::random();
                if a<p{
                    graph.entry(u).or_insert(Vec::new()).push(v);
                    graph.entry(v).or_insert(Vec::new()).push(u);
                }
            }
        }
    }
    return graph;
}

// Utility struc for UPA algorithm
struct UPATrial {
    numNodes: i32,
    nodeNumbers: Vec<i32>,
}

// methods for UPATrial
impl UPATrial{

    // default constructor
    fn new()->UPATrial{
        UPATrial {numNodes: 0,nodeNumbers: Vec::new(),}
    }

    // constructor
    fn m(&mut self,m: i32)->&mut UPATrial{
        self.numNodes = m;
        for i in 0..m {
            for _ in 0..m {
                self.nodeNumbers.push(i);
            }
        }
        return self;
    }

    // run a trial and give ther resulting extracted nodes
    fn run_trial(&mut self,m:i32)->Vec<i32>{
        let mut V = Vec::new();
        rand::thread_rng().shuffle(&mut self.nodeNumbers);
        for i in 0..m {
            let u = self.nodeNumbers.pop().unwrap();
            V.push(u);
        }
        self.nodeNumbers.push(self.numNodes);
        for v in &V {
            self.nodeNumbers.push(*v);
        }
        return V;
    }
}

// generate a random graph with n nodes
fn upa(n:i32,m:i32)->HashMap<i32,Vec<i32>>{
    let mut graph = HashMap::new();
    for u in 0..m {
        graph.insert(u,Vec::new());
        for v in 0..m {
            if v != u {
                graph.entry(u).or_insert(Vec::new()).push(v);
            }
        }
    }
    let mut trial = UPATrial::new();
    trial.m(m);
    for u in m..n {
        let V = trial.run_trial(m);
        for v in V {
            graph.entry(u).or_insert(Vec::new()).push(v);
            graph.entry(v).or_insert(Vec::new()).push(u);
        }
    }
    return graph;
}

// return the number of nodes and edges of a graph
fn shape(graph: &HashMap<i32,Vec<i32>>)->(usize,usize){
    let mut nodes = 0;
    let mut edges = 0;
    for (_,e) in graph {
        nodes = nodes+1;
        edges = edges+e.len();
    }
    return (nodes,edges/2);
}

// return the list of nodes of a graph
fn get_nodes(graph: &HashMap<i32,Vec<i32>>)->Vec<i32>{
    let mut nodes = Vec::new();
    for v in graph.keys(){
        nodes.push(*v);
    }
    return nodes;
}

// remove a node from a graph and all its edges
fn remove_node(graph: &mut HashMap<i32,Vec<i32>>,sel: i32){
    let adj = graph.remove(&sel).unwrap();
    for u in adj {
        let mut xs = graph.entry(u).or_insert(Vec::new());
        let index = xs.iter().position(|x| *x == sel).unwrap();
        xs.remove(index);
    }
}

#[derive(PartialEq)]
enum ColorG {
    White,
    Gray,
    Black,
}

// return a vector with the connected components of a graph
fn connected_components(graph: & HashMap<i32,Vec<i32>>)->Vec<Vec<i32>>{
    let mut color: HashMap<i32,ColorG> = HashMap::new();
    for v in get_nodes(&graph) {
        color.insert(v,ColorG::White);
    }
    let mut cc: Vec<Vec<i32>> = Vec::new();
    for v in get_nodes(&graph) {
        if *(color.get(&v).unwrap()) == ColorG::White {
            let mut visited: Vec<i32> = Vec::new();
            let comp = dfs_visited(&graph,&mut color,v,&mut visited);
            cc.push(comp.to_vec());
        }
    }
    return cc;
}

// explore a graph in depht
fn dfs_visited<'a>(graph: & HashMap<i32,Vec<i32>>,
        color: &mut HashMap<i32,ColorG>,
        u: i32,visited:&'a mut Vec<i32>)->&'a mut Vec<i32> {
        color.insert(u,ColorG::Gray);
        visited.push(u);
        for v in graph.get(&u).unwrap() {
            if *(color.get(&v).unwrap())==ColorG::White {
                dfs_visited(&graph,color,*v,visited);
            }
        }
        color.insert(u,ColorG::Black);
        return visited;
    }

// return the number of nodes inside the biggest connected component
// divided by the total number of nodes in the graph
fn connettivita(cc:&Vec<Vec<i32>>,n:usize)->f64{
    let mut cmax = 0f64;
    for comp in cc {
        let mut c = 0f64;
        for _ in comp {
            c = c + 1f64;
        }
        if c>cmax {
            cmax = c;
        }
    }
    return cmax/(n as f64);
}

// return the number of nodes inside the biggest connected component of
// the graph
fn resilienza(cc:&Vec<Vec<i32>>)->f64{
    let mut cmax = 0f64;
    for comp in cc {
        let mut c = 0f64;
        for _ in comp {
            c = c + 1f64;
        }
        if c>cmax {
            cmax = c;
        }
    }
    return cmax;
}

// disable one by one all nodes in the graph, choosend in a random way,
// and return the result of calling resilienza at each time
fn attack(mut graph: &mut HashMap<i32,Vec<i32>>)->Vec<f64>{
    println!("Simulo attacchi..");
    let mut keys = get_nodes(&graph);
    let mut conn: Vec<f64> = Vec::new();
    let (n,e) = shape(&graph);
    while keys.len()>1 {
        let a = rand::thread_rng().gen_range(0,keys.len());
        let sel = keys[a];
        // println!("sel:{} (from a:{})",sel,a);
        remove_node(&mut graph,sel);
        // println!("as19991212 n:{} e:{}",n,e);
        keys.remove(a);
        let cc = connected_components(&graph);
        conn.push(resilienza(&cc));//connettivita(&cc,n));
    }
    return conn;
}

// disable one by one all nodes in the graph, choosing at each time
// the one with the biggest number of edges,
// and return the result of calling resilienza
fn structural_attack(mut graph: &mut HashMap<i32,Vec<i32>>)->Vec<f64>{
    println!("Simulo attacchi strutturali..");
    let mut keys = get_nodes(&graph);
    let mut conn: Vec<f64> = Vec::new();
    let (n,e) = shape(&graph);
    while keys.len()>1 {
        let mut a = 0;
        let mut sel = keys[a];
        let mut deg = 0;
        for i in 0..keys.len() {
            let u = keys[i];
            let d = graph.get(&u).unwrap().len();
            if d>deg {
                deg = d;
                a = i;
                sel = u;
            }
        }
        // println!("sel:{} (from a:{})",sel,a);
        remove_node(&mut graph,sel);
        // println!("as19991212 n:{} e:{}",n,e);
        keys.remove(a);
        let cc = connected_components(&graph);
        conn.push(resilienza(&cc));//connettivita(&cc,n));
    }
    return conn;
}

fn main() {
    // load the real network
    let mut graph = read_graph(String::from("as19991212.txt"));
    let (n1,e1) = shape(&graph);
    let x1 = linspace(1f64, n1 as f64, n1 as u64);
    println!("as19991212 \t n: {} \t e: {}",n1,e1);

    // generate a random network with ER algorithm
    let mut er_graph = er(1476,0.0016);
    let (n2,e2) = shape(&er_graph);
    let x2 = linspace(1f64, n2 as f64, n2 as u64);
    println!("er-generated \t n: {} \t e: {}",n2,e2);

    // generate a random network with UPA algorithm
    let mut upa_graph = upa(1476,2);
    let (n3,e3) = shape(&upa_graph);
    let x3 = linspace(1f64, n3 as f64, n3 as u64);
    println!("upa-generated \t n: {} \t e: {}",n3,e3);

    // attack all networks with random attack
    // let resilienza1: Vec<f64> = attack(&mut graph);
    // let res_er: Vec<f64> = attack(&mut er_graph);
    // let res_upa: Vec<f64> = attack(&mut upa_graph);

    // attack all networks with structural attack
    let resilienza1: Vec<f64> = structural_attack(&mut graph);
    let res_er: Vec<f64> = structural_attack(&mut er_graph);
    let res_upa: Vec<f64> = structural_attack(&mut upa_graph);

    // plot the results
    let mut fg = Figure::new();
    fg.axes2d()
        .lines(&x1, &resilienza1,
            &[Caption("Resilienza rete reale"), Color("black")])
        .lines(&x1, &res_er,
            &[Caption("Resilienza rete ER"), Color("blue")])
        .lines(&x3, &res_upa,
            &[Caption("Resilienza rete UPA"), Color("red")]);
    fg.show();
}
