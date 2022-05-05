user_know_level(PEG,LPR,_,_,_,'Very Low'):-not(PEG>0.38),not(PEG>0.13),not(LPR>0.62).
user_know_level(PEG,LPR,_,_,_,'Low'):-not(PEG>0.38),not(PEG>0.13),(LPR>0.62).
user_know_level(PEG,_,_,_,_,'Low'):-not(PEG>0.38),(PEG>0.13).
user_know_level(PEG,LPR,_,_,_,'MiddLe'):-(PEG>0.38),not(PEG>0.68),not(LPR>0.83).
user_know_level(PEG,LPR,_,_,_,'High'):-(PEG>0.38),not(PEG>0.68),(LPR>0.83).
user_know_level(PEG,_,_,_,_,'High'):-(PEG>0.38),(PEG>0.68).