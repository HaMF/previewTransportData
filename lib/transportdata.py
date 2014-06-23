# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 13:32:51 2014

Shared functions for processing transport measurement data.

@author: hannes.maierflaig
"""

import numpy as np
    
def symmetrizeSignalZero(y, idx = None):
    """
    Dischard antisymmetric (around center index or around idx) part by 
    taking the sum of the signal at x[idx_centre +n] and x[idx_centre -n]
    
    Parameters
    ----------
    y: numpy array or list of data values to symmetrize
    idx: index of center to symmetrize around if ommitted len(y)/2 is taken as idx
    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y = np.array(y)
    if not np.size(y)%2:
        raise Exception("Data needs to have an uneven number of elements if no center index (idx) is provided")
    if not idx:
        idx = np.size(y)/2
        idx_end = np.size(y)
    else:
        idx_end = min((np.size(y), idx*2))
        
    y = (y[0:idx] + y[idx+1:idx_end][::-1])/2
    return y


def antiSymmetrizeSignalZero(y, idx = None):
    """
    Dischard symmetric (around center index or around idx) part by 
    taking the difference of the signal at x[idx_centre +n] and x[idx_centre -n]
        
    Parameters
    ----------
    y: numpy array or list of data values to anti symmetrize
    idx: index of center to symmetrize around if ommitted len(y)/2 is taken as idx    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y = np.array(y)
    if not np.size(y)%2:
        raise Exception("Data needs to have an uneven number of elements if no center index (idx) is provided")
    if not idx:
        idx = np.size(y)/2
        idx_end = np.size(y)
    else:
        idx_end = min((np.size(y), idx*2))
        
    y = (y[0:idx] - y[idx+1:idx_end][::-1])/2
    return y
    
    
def antiSymmetrizeSignal(y, symmetryStep):
    """    
    Dischard symmetric (around center index or around idx) part of a signal by 
    taking the difference of the signal at x[idx_centre +n] and x[idx_centre +n + symmetry_step]
    get your corresponding x data as x[0:len(y)/]
            
    Parameters
    ----------
    y: numpy array or list of data values to anti symmtetrize
    symmetryStep: expected symmetry of the signal at x[n] occurs at x[n+symmetryStep]
    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y = np.array(y)
    if np.size(y)%2:
        raise Exception("Data needs to have an even number of elements")
        
    s = np.zeros(len(y)/2)
    for idx in range(0,len(y)/2):
        s[idx] = (y[idx] - y[idx+symmetryStep])/2
    return s


def symmetrizeSignal(y, symmetryStep):
    """
    Dischard antisymmetric (around center index or around idx) part of a signal by 
    taking the sum of the signal at x[idx_centre +n] and x[idx_centre +n + symmetry_step].
    
    Get your corresponding x data as x[0:len(y)/]
    
    Parameters
    ----------
    y: numpy array or list of data values to anti symmtetrize
    symmetryStep: expected symmetry of the signal at x[n] occurs at x[n+symmetryStep]
    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y = np.array(y)
    if np.size(y)%2:
        raise Exception("Data needs to have an even number of elements")
        
    s = np.zeros(len(y)/2)
    for idx in range(0,len(y)/2):
        s[idx] = (y[idx] + y[idx+symmetryStep])/2
    return s


def symmetrizeSignalUpDown(y, symmetryStep):
    """
    Symmetrize a signal that is recorded as an up and down sweep by calculating
    the cross sum between up and down sweep of values shifted by symmetry step.
    
    Get the corresponding x data as averageUpDownSweep(x).
    
    Parameters
    ----------
    y: numpy array or list of data values to anti symmtetrize
    symmetryStep: expected symmetry of the signal at x[n] occurs at x[n+symmetryStep]
    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y=np.array(y)
    yL = np.hstack((y[0:len(y)/4],y[2*len(y)/4:3*len(y)/4]))
    yU = np.hstack((y[len(y)/4:2*len(y)/4],y[3*len(y)/4:]))
    
    y_sym = np.hstack((symmetrizeSignal(yL, symmetryStep), symmetrizeSignal(yU, symmetryStep)))
    
    
    return y_sym
    

def antiSymmetrizeSignalUpDown(y, symmetryStep):
    """
    Antisymmetrize a signal that is recorded as an up and down sweep by calculating
    the cross difference between up and down sweep of values shifted by symmetry step.
    
    Get the corresponding x data as averageUpDownSweep(x).
    
    Parameters
    ----------
    y: numpy array or list of data values to anti symmtetrize
    symmetryStep: expected symmetry of the signal at x[n] occurs at x[n+symmetryStep]
    
    Returns
    ----------
    y_symmetrized: numpy array of dimension size(y)/2
    """
    y=np.array(y)
    yL = np.hstack((y[0:len(y)/4],y[2*len(y)/4:3*len(y)/4])) 
    yU = np.hstack((y[len(y)/4:2*len(y)/4],y[3*len(y)/4:]))
    
    y_sym = np.hstack((antiSymmetrizeSignal(yL, symmetryStep), antiSymmetrizeSignal(yU, symmetryStep)))
    
    return y_sym
    
def separateAlternatingSignal(x):
    """
    Separates each 2nd element of an array into two array

    Returns    
    ----------
    separated_signal: list of two arrays (x[2n], x[2n-1])
    """
    return np.array(x[0::2]), np.array(x[1::2])