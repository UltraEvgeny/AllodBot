

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
	local unit_has_buff = false
	for i = 1, #target_buff_list do
		if (userMods.FromWString(object.GetBuffInfo(target_buff_list[i]).name) == buffName) then
			unit_has_buff = true
		end
	end
	return unit_has_buff
end

function spellInCd(spellName)
	local spell_cd
	for i, id in pairs( avatar.GetSpellBook() ) do
		if userMods.FromWString(spellLib.GetDescription(id).name) == spellName then
			spell_cd = spellLib.GetCooldown(id).remainingMs
		end
	end
	local spell_in_cd = 0
	if spell_cd > 300 then
		spell_in_cd = 1
	end
	return spell_in_cd
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
	local target_is_invul = 0
	local target_health_info = object.GetHealthInfo(targetId)
	if target_health_info then
		target_is_invul = target_health_info.isInvulnerable and 1 or 0
	end

	if avatar_angle < 0 then avatar_angle = avatar_angle + 2*math.pi end
	if camera_angle < 0 then camera_angle = camera_angle + 2*math.pi end
	local is_mounted_mirag = 0
	local active_mount_id = mount.GetActive()
	if active_mount_id and userMods.FromWString(mount.GetInfo(active_mount_id).name)=="Мираж" then is_mounted_mirag=1 end

	
	if avatarPos then
		local mapId = unit.GetZonesMapId(avatarId) 
		local geodata = mapId and cartographer.GetObjectGeodata( avatarId, mapId )
		state1 = string.format( 
			[[X %d X %d X %d X %d X %d]],

			avatarPos.posX,
			avatarPos.posY,
			object.GetHealthInfo(avatarId).valuePercents,
			avatar_angle*100,
			camera_angle*100
		)
		state2 = string.format(
			[[X %d%d%d %d %d%d%d%d%d%d%d%d%d%d]]
			----- mask start
			,avatar.IsAlive() and 1 or 0 --# is_alive
			,object.IsInCombat(avatarId) and 1 or 0 --# is_combat_me
			,object.IsInCombat(targetId) and 1 or 0 --# is_combat_target
			,target_is_invul --# is_invul_target
			,unit.IsPlayer( targetId ) and 1 or 0 --# target_is_hero
			,is_mounted_mirag --# is_mounted
			,unitHasBuff(avatarId, "Могильный холод") and 1 or 0 --# has_mogilnii_holod
			,unitHasBuff(avatarId, "Кровопускание") and 1 or 0 --# has_krovopuskanie
			,unitHasBuff(targetId, "Алчные тени") and 1 or 0 --# target_has_alch
			,unitHasBuff(targetId, "Лихорадка") and 1 or 0 --# target_has_lih
			,unitHasBuff(targetId, "Нейротоксин") and 1 or 0 --# target_has_neurotoxin
			,unitHasBuff(targetId, "Вирус") and 1 or 0 --# target_has_virus
			,spellInCd("Алчные тени") --# is_alch_in_cd
			,spellInCd("Кровопускание") --# is_krovopuskanie_in_cd
			----- mask end

		)
	end
	wtMessage:SetVal( "value", state1 )
	wtMessage2:SetVal( "value", state2 )
	
	wtMessage3:SetVal( "value", string.format("%d", avatar.GetNecromancerBloodPool().value ))
	-- wtMessage3:SetVal( "value", string.format("%d", spellLib.GetCooldown(avatar.GetSpellBook()[60]).remainingMs  ))
	-- wtMessage3:SetVal( "value", userMods.FromWString(spellLib.GetDescription(avatar.GetSpellBook()[60]).name))
	-- wtMessage3:SetVal( "value", userMods.FromWString(zone.zoneName) )
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
	common.RegisterEventHandler( Update, "EVENT_SECOND_TIMER" )


	wtMessage = mainForm:GetChildChecked( "Row1", false )
	wtMessage2 = mainForm:GetChildChecked( "Row2", false )
	wtMessage3 = mainForm:GetChildChecked( "Row3", false )

	Update()
end
--------------------------------------------------------------------------------
Init()
--------------------------------------------------------------------------------
