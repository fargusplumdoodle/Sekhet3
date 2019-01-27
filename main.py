rclone = Backup.Rclone_Wrapper(log_file='/tmp/backup.log')

rclone.dirs = ['test']

rclone.run()

