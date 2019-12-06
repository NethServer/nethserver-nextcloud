# nextcloud.rb

require 'rubygems'

Facter.add('nextcloud') do
    setcode do
        nextcloud = {}
        users = Facter::Core::Execution.exec("su - apache -s /bin/bash -c \"source /opt/rh/rh-php72/enable; cd /usr/share/nextcloud/; php occ user:list | wc -l \"")
        nextcloud['users'] = users.to_i
        size = Facter::Core::Execution.exec("du -s /var/lib/nethserver/nextcloud/")
        nextcloud['size'] = size.to_i
        nextcloud
    end
end
