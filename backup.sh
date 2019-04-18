#!/bin/bash

DATE=$(date +%Y%b%d_%H:%m:%S)
target_dir="/Monitoring/nagios"
#remote_path="/Monitoring/Nagios_Backup"
#filename=log_back_$timestamp.txt
log="log/nagios_backup_log_$DATE.txt"
key="/home/ngbkp/.ssh/id_rsa.pub"
remote_user="ngbkp"
remote_host=""
hostname=$HOSTNAME
remote_path="/Monitoring/Nagios_Backup/$hostname"


#find $path -name "*.txt"  -type f -mtime +7 -print -delete >> $log

sudo echo "Backup:: Script Start -- $DATE" >> $log

START_TIME=$(date +%s)

echo "....................Deleting 7 days old archive..................." >> $log
ssh -o StrictHostKeyChecking=no  $remote_host "if [ -d "$remote_path" ]; then sudo find $remote_path  -mtime +15 -print -delete; else sudo mkdir $remote_path; fi"
#ssh $remote_host "sudo mkdir $remote_path/$hostname"
#rsync -avh ssh $target_dir $remote_user@$remote_host:/$remote_path/$hostname | tee -a  $log    

ssh -o StrictHostKeyChecking=no  $remote_host "sudo chmod -R 777 $remote_path"


echo "....................Remote File tranfer initiated................." >> $log
rsync -avh ssh $target_dir $remote_user@$remote_host:/$remote_path | tee -a  $log
#ssh  $remote_host "sudo tar -czvf nagios_$(date +%Y%b%d).tar.gz $remote_path/nagios" | tee -a $log

echo "...............Archiving the file remotely to reduce size.........." >> $log
ssh  $remote_host "sudo tar -czvf $remote_path/nagios_$(date +%Y%b%d)tar.gz $remote_path/nagios" | tee -a $log

if [ $? -eq 0 ];then
echo "Archived Successful" >> $log
else
echo "Please login to the system and check" >> $log
fi

echo "...............cleaning up the nagios folder after Archiving......" >> $log

ssh -o StrictHostKeyChecking=no  $remote_host "if [ -f $remote_path/nagios_$(date +%Y%b%d)tar.gz ]; then sudo rm -rf $remote_path/nagios; fi"

END_TIME=$(date +%s)

ELAPSED_TIME=$(expr $END_TIME - $START_TIME)


echo "Backup :: Script End -- $(date +%Y%m%d_%H%M)" >> $log
#echo "Elapsed Time ::  $(date -d 00:00:$ELAPSED_TIME +%Hh:%Mm:%Ss)"  >> $log
total_time=$(echo $(($END_TIME-$START_TIME)) | awk '{print int($1/60)":"int($1%60)}')
#total_time=$(expr $ELAPSED_TIME | awk '{print int($1/60)":"int($1%60)}')
echo "Elapsed Time :: $total_time" >> $log
