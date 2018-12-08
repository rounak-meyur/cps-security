# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 21:45:40 2018

Author: Rounak Meyur
"""

import sys
import networkx as nx
import numpy as np
import itertools


def set_individual(vul_list):
    '''
    Find the individual probability of each element.
    Input: a list [a,b,c]
    Output: a list [a(1-b)(1-c),(1-a)b(1-c),(1-a)(1-b)c]
    '''
    V = []
    for i in range(len(vul_list)):
        p_list = [vul_list[i]]+[(1-vul_list[j]) for j in range(len(vul_list)) if i!=j]
        V.append(np.prod(p_list))
    return V


def set_union(vul_list):
    '''
    '''
    S = 0
    for i in range(len(vul_list)):
        S += ((-1)**i)*sum([np.prod(l) for l in list(itertools.combinations(vul_list,i+1))])
    return S


def ComputeEdgeExploit(G,CVSS,vul_type,k):
    '''
    Computes the probability of successful exploit of every vulnerability
    Input: Networkx Graph G
    '''
    Edge_Exp = {}; Time_Compromise = {}  
    vul_list = list(G.edges(keys=True))
    for v in vul_list:
        # Compute the probability of successful exploit
        s = np.random.uniform(low=0.8,high=1.0)
        n = np.random.uniform(low=0.8,high=1.0)
        Edge_Exp[v] = (CVSS[v[2]]/10.0)*s*n
        
        # Compute time to compromise
        if vul_type[v[2]] == 'K':
            Time_Compromise[v]=(10/CVSS[v[2]])*(1+(4.8*np.exp(-k)))
        elif vul_type[v[2]] == 'Z':
            Time_Compromise[v]=32+(10/CVSS[v[2]])+(33+(4.8*10/CVSS[v[2]]))*np.exp(-k)
        else:
            print "Wrong code of vulnerability!!!... Exiting program"
            sys.exit(0)
    nx.set_edge_attributes(G,Edge_Exp,'exploit')
    nx.set_edge_attributes(G,Time_Compromise,'compromise')
    return
    

def ComputeNodeExploit(G):
    '''
    '''
    Node_Exp = {}; Ind_Edge_Exp = {}
    Edge_Exp = nx.get_edge_attributes(G,'exploit')
    
    nd = [n for n in list(G.nodes()) if G.in_degree(n)==0][0]
    Node_Exp[nd] = 1.0
    
    node_list = list(G.nodes())
    calculated = [nd]; node_list.remove(nd)
    
    while len(node_list) != 0:
        dict_pred = {n:list(G.predecessors(n)) for n in node_list}
        # identify the nodes for which calculation can be done
        current_node = [n for n in dict_pred if len(set(dict_pred[n])-set(calculated))==0]
        for nd in current_node:
            comp_exploit = []
            for pred in list(G.predecessors(nd)):
                # get the incoming edges to the node
                edge_list = [e for e in list(set(G.out_edges(pred,keys=True))\
                            .intersection(set(G.in_edges(nd,keys=True))))]
                vul_list = [Edge_Exp[e] for e in edge_list]
                # get the probability of successful exploit of the succeeding node
                comp_exploit.append(Node_Exp[pred]*set_union(vul_list))
                # get the individual probability of exploit for each vulnerability
                ind_vul_list = set_individual(vul_list)
                for i in range(len(vul_list)):
                    Ind_Edge_Exp[edge_list[i]] = ind_vul_list[i]*Node_Exp[pred]
            # update the exploit of the current node
            Node_Exp[nd] = set_union(comp_exploit)
            # add the computed node to the list and remove it from total nodelist
            calculated.append(nd); node_list.remove(nd)
        
    nx.set_edge_attributes(G,Ind_Edge_Exp,'ind_exploit')
    nx.set_node_attributes(G,Node_Exp,'exploit')
    return


def ComputeTimeCompromise(G):
    '''
    '''
    TTC = nx.get_edge_attributes(G,'compromise')
    ind_P = nx.get_edge_attributes(G,'ind_exploit')
    Exploit = nx.get_node_attributes(G,'exploit')
    MTTC_node = {}
    nd = [n for n in list(G.nodes()) if G.in_degree(n)==0][0]
    MTTC_node[nd] = 0.0
    
    node_list = list(G.nodes())
    calculated = [nd]; node_list.remove(nd)
    
    while len(node_list) != 0:
        dict_pred = {n:list(G.predecessors(n)) for n in node_list}
        # identify the nodes for which calculation can be done
        current_node = [n for n in dict_pred if len(set(dict_pred[n])-set(calculated))==0]
        for nd in current_node:
            S = 0
            for pred in list(G.predecessors(nd)):
                # get the incoming edges to the node
                edge_list = [e for e in list(set(G.out_edges(pred,keys=True)).\
                                             intersection(set(G.in_edges(nd,keys=True))))]
                S += sum([(MTTC_node[pred]+TTC[v])*ind_P[v] for v in edge_list])/Exploit[nd]
            # update the MTTC of the current node
            MTTC_node[nd] = S
            # add the computed node to the list and remove it from total nodelist
            calculated.append(nd); node_list.remove(nd)
    nx.set_node_attributes(G,MTTC_node,'MTTC')
    
    goal = [n for n in list(G.nodes()) if G.out_degree(n)==0][0]
    return MTTC_node[goal]


def ModelA(CVSS,vul_type,k):
    '''
    LAN model A: The intruder (user_ext) attacks the workstation and gains access
    (user_HMI) by bypassing the firewall either through ftp or ssh vulnerability.
    The ftp vulnerability is a known vulnerability and the ssh is a zero-day one.
    The final vulnerability to gain root access at the HMI (root_HMI) is a known
    vulnerability.
    '''
    G = nx.MultiDiGraph()
    G.add_edge('user_ext','user_HMI',key='ftp')
    G.add_edge('user_ext','user_HMI',key='ssh')
    G.add_edge('user_HMI','root_HMI',key='bof')
    
    ComputeEdgeExploit(G,CVSS,vul_type,k)
    ComputeNodeExploit(G)
    MTTC = ComputeTimeCompromise(G)
    return MTTC


def ModelB(CVSS,vul_type,k):
    '''
    LAN model B: There is a shared server which connects two virtual LANS.The 
    intruder (user_ext) can attack the workstation directly and gains access
    (user_HMI) by bypassing the firewall either through ftp or ssh vulnerability.
    In other case, he can gain access of the server (user_svr) and then access
    the HMI. The ftp vulnerability is a known vulnerability and the ssh is a 
    zero-day one. The final vulnerability to gain root access at the HMI 
    (root_HMI) is a known vulnerability.
    '''
    G = nx.MultiDiGraph()
    G.add_edge('user_ext','user_svr',key='xss')
    G.add_edge('user_svr','user_HMI',key='ftp')
    G.add_edge('user_svr','user_HMI',key='ssh')
    G.add_edge('user_ext','user_HMI',key='ftp')
    G.add_edge('user_ext','user_HMI',key='ssh')
    G.add_edge('user_HMI','root_HMI',key='bof')
    
    ComputeEdgeExploit(G,CVSS,vul_type,k)
    ComputeNodeExploit(G)
    MTTC = ComputeTimeCompromise(G)
    return MTTC


def ModelC(CVSS,vul_type,k):
    '''
    LAN model C: There is a local SCADA which connects the HMIs.The intruder 
    (user_ext) can attack the local SCADA through a http vulnerability and gain
    access (user_scd) by bypassing the firewall. Thereafter he can exploit ftp 
    or ssh vulnerability to access the HMI (user_HMI). The ftp vulnerability is
    a known vulnerability and the ssh is a zero-day one. The final vulnerability
    to gain root access at the HMI (root_HMI) is a known vulnerability.
    '''
    G = nx.MultiDiGraph()
    G.add_edge('user_ext','user_scd',key='htp')
    G.add_edge('user_scd','user_HMI',key='ftp')
    G.add_edge('user_scd','user_HMI',key='ssh')
    G.add_edge('user_HMI','root_HMI',key='bof')
    
    ComputeEdgeExploit(G,CVSS,vul_type,k)
    ComputeNodeExploit(G)
    MTTC = ComputeTimeCompromise(G)
    return MTTC


def ModelCC(CVSS,vul_type,k):
    '''
    Control Center:
    '''
    G = nx.MultiDiGraph()
    G.add_edge('user_ext','user_dat',key='dos')
    G.add_edge('user_ext','user_dat',key='exe')
    G.add_edge('user_dat','user_app',key='ssh')
    G.add_edge('user_app','root_app',key='bof')
    
    ComputeEdgeExploit(G,CVSS,vul_type,k)
    ComputeNodeExploit(G)
    MTTC = ComputeTimeCompromise(G)
    return MTTC


































