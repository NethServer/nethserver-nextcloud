#
# Copyright (C) 2020 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

require 'rubygems'
require 'json'

Facter.add('nextcloud') do
    setcode do
        users_count = 0
        begin
            admin = Facter::Core::Execution.execute("/sbin/e-smith/config getprop admins user", :timeout => 10)
        rescue Facter::Core::Execution::ExecutionFailure
            admin = "admin"
        end
        begin
            # Count nextcloud users, excluding "admin", "admin@" and never-logged-in users
            users_list = Facter::Core::Execution.execute("occ user:list -i --output=json", :timeout => 30)
            JSON.parse(users_list).each do |uid, item|
                next if uid == "admin"
                next if item["email"][0..5] == admin + "@" and item["backend"] != "Database"
                next if item["last_seen"] == "1970-01-01T00:00:00+00:00"
                users_count += 1
            end
        rescue Facter::Core::Execution::ExecutionFailure
            users_count = nil
        rescue JSON::ParserError
            users_count = nil
        end
        nextcloud = { "users" => users_count }
    end
end
