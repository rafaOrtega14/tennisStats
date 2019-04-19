SELECT 'ID1','ID2','ID_T','ID_R','FS_1','FSOF_1','ACES_1','DF_1','UE_1','W1S_1','W1SOF_1','WIS_1','W2S_1','W2SOF_1','BP_1','BPOF_1',
'NA_1','NAOF_1', 'TPW_1','FAST_1','AIS_1','AIS_2','FS_2','FSOF_2','ACES_2','DF_2','UE_2','W1S_2','W1SOF_2','WIS_2','WISOF_2','WIS_2',
'BP_2', 'BPOF_2','NA_2','NAOF_2','TPW_2','FAST_2','A1S_2','A2S_2','RPW_1','RPWOF_1','RPW_2','RPWOF_2','MT','ID_C','NAME_C','RESULT_G'  
UNION SELECT stat_atp.*,courts.*,games_atp.RESULT_G FROM stat_atp INNER JOIN tours_atp ON tours_atp.ID_T=stat_atp.ID_T INNER JOIN 
courts ON courts.ID_C=tours_atp.ID_C_T INNER JOIN games_atp ON games_atp.ID1_G=stat_atp.ID1 AND games_atp.ID2_G=stat_atp.ID2 AND 
games_atp.ID_T_G=stat_atp.ID_T INTO OUTFILE '/var/lib/mysql-files/TENNIS.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' 
ESCAPED BY '"' LINES TERMINATED BY '\r\n';