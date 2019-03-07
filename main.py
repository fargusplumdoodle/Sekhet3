
#rclone.dirs = ['test']

import Backup

rclone = Backup.Rclone_Wrapper()
rclone.run()
#rsync = Backup.Rsync_Wrapper()

#rsync.run()
