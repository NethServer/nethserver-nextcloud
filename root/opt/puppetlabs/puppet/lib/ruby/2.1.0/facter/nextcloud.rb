# nextcloud.rb

require 'rubygems'

Facter.add('nextcloud') do
    setcode do
        nextcloud = {}
        pass = File.read("/var/lib/nethserver/secrets/nextcloud").strip
        users = Facter::Core::Execution.exec("mysql -BN -u nextcloud -p#{pass} nextcloud -e \"select count(*) from oc_accounts where uid != 'admin'\"")
        nextcloud['users'] = users.to_i
        size = Facter::Core::Execution.exec("du -s /var/lib/nethserver/nextcloud/")
        nextcloud['size'] = size.to_i
        nextcloud
    end
end
