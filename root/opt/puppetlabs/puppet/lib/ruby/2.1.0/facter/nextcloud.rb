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

Facter.add('nextcloud') do
    setcode do
        # Count nextcloud users, excluding "admin", "admin@" and never-logged-in users
        users = Facter::Core::Execution.execute("occ user:list -i --output=json  | jq 'map(if .email[0:6] != \"admin@\" and .user_id != \"admin\" and .last_seen != \"1970-01-01T00:00:00+00:00\" then . else empty end) | length'", :timeout => 30)
        nextcloud = { "users" => users.to_i }
    end
end
