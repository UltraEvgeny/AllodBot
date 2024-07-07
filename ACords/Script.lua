

-- WIDGETS
Global( "wtMessage", nil )
Global( "wtMessage2", nil )
Global( "wtMessage3", nil )

-- OTHER
Global( "fadeStatus", WIDGET_FADE_TRANSPARENT )

--------------------------------------------------------------------------------
-- EVENT HANDLERS
--------------------------------------------------------------------------------

function unitHasBuff (unitId, buffName)
	local target_buff_list = object.GetBuffs(unitId)
	local unit_has_neurotoxin = false
	for i = 1, #target_buff_list do
		if (userMods.FromWString(object.GetBuffInfo(target_buff_list[i]).name) == buffName) then
			unit_has_neurotoxin = true
		end
	end
	return unit_has_neurotoxin
end


-- EVENT_AVATAR_CLIENT_ZONE_CHANGED
function Update(params)

	local avatarId = avatar.GetId()
	
	if not avatarId then return end
	local targetId = avatar.GetTarget()
	local targetProj = object.GetInstantProjectedInfo(targetId)
	local avatarPos = avatarId and avatar.GetPos()
	local state1 = "-- : --"
	local state2 = "-- : --"
	local detectedObjects = avatar.GetDetectedObjects()
	local zone = cartographer.GetCurrentZoneInfo()
	local avatar_angle = avatar.GetDir()
	local camera_angle = mission.GetCameraDirection()

	if avatar_angle < 0 then avatar_angle = avatar_angle + 2*math.pi end
	if camera_angle < 0 then camera_angle = camera_angle + 2*math.pi end
	local is_mounted_mirag = 0
	local active_mount_id = mount.GetActive()
	if active_mount_id and userMods.FromWString(mount.GetInfo(active_mount_id).name)=="Мираж" then is_mounted_mirag=1 end

	local target_has_alch = unitHasBuff(targetId, "Алчные тени")
	local target_has_lih = unitHasBuff(targetId, "Лихорадка")
	local target_has_neurotoxin = unitHasBuff(targetId, "Нейротоксин")
	
	local is_nearby_enemy_combat_unit_without_neurotoxin = false
	local unitIds = avatar.GetUnitList()
	for _, unitId in ipairs(unitIds) do
		if object.IsEnemy(unitId) and object.IsInCombat(unitId) and not unitHasBuff(unitId, "Нейротоксин") then
			is_nearby_enemy_combat_unit_without_neurotoxin = true
		end
	end


	if avatarPos then
		local mapId = unit.GetZonesMapId(avatarId) 
		local geodata = mapId and cartographer.GetObjectGeodata( avatarId, mapId )
		state1 = string.format( 
			[[X %d X %d X %d X %d X %d X %d X %d]],
			avatar.IsAlive() and 1 or 0,
			avatarPos.posX,
			avatarPos.posY,
			avatar_angle*100,
			object.IsInCombat(avatarId) and 1 or 0,
			object.IsInCombat(targetId) and 1 or 0,
			unit.IsPlayer( targetId ) and 1 or 0			
		)
		state2 = string.format( 
			[[X %d X %d X %d X %d%d%d X %d X %d]],
			object.GetHealthInfo(avatarId).valuePercents,
			camera_angle*100,
			--avatar.GetTarget() or 0,
			is_mounted_mirag,
			target_has_alch and 1 or 0, target_has_lih and 1 or 0, target_has_neurotoxin and 1 or 0,
			is_nearby_enemy_combat_unit_without_neurotoxin and 1 or 0,
			unitHasBuff(avatarId, "Могильный холод") and 1 or 0
		)
	end
	wtMessage:SetVal( "value", state1 )
	wtMessage2:SetVal( "value", state2 )
	wtMessage3:SetVal( "value", userMods.FromWString(zone.zoneName) )
end


--------------------------------------------------------------------------------
-- INITIALIZATION
--------------------------------------------------------------------------------
function Init()
	common.RegisterEventHandler( Update, "EVENT_AVATAR_CLIENT_ZONE_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_AVATAR_POS_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_AVATAR_ZONE_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_AVATAR_DIR_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_TARGET_POS_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_AVATAR_TARGET_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_CAMERA_DIRECTION_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_ACTIVE_MOUNT_CHANGED" )
	common.RegisterEventHandler( Update, "EVENT_OBJECT_BUFF_ADDED" )
	common.RegisterEventHandler( Update, "EVENT_OBJECT_BUFF_REMOVED" )


	wtMessage = mainForm:GetChildChecked( "Row1", false )
	wtMessage2 = mainForm:GetChildChecked( "Row2", false )
	wtMessage3 = mainForm:GetChildChecked( "Row3", false )

	Update()
end
--------------------------------------------------------------------------------
Init()
--------------------------------------------------------------------------------
