-- Insert data into Utilisateur
-- Password user1 : Test111!
INSERT INTO ProjetInfo.Utilisateur (id_user, mdp_hashe, date_naissance, nom, prenom, pseudo)
VALUES
('IUSZEM', 'df45a38d72964fbe867eaaf20589bdcb394c0f4b680760b91097ee3f78170c43', '1111-11-11', 't', 't', 't'),
('user2', 'hashedpassword2', '1985-05-15', 'Smith', 'Jane', 'jane_smith');

-- Insert data into Sounddeck
INSERT INTO ProjetInfo.Sounddeck (id_sd, nom, description, date_creation, id_createur)
VALUES
('sd1', 'Fantasy Ambience', 'A mystical sounddeck for fantasy RPGs.', '2024-01-01', 'IUSZEM'),
('sd2', 'Sci-fi Sounds', 'Futuristic sound effects for space adventures.', '2024-01-02', 'IUSZEM'),
('sd3', 'Horror Atmosphere', 'Spooky sounds for horror games.', '2024-01-03', 'IUSZEM'),
('sd4', 'Nature Sounds', 'Relaxing nature-themed sounddeck.', '2024-01-01', 'user2'),
('sd5', 'City Ambience', 'Urban sounds for city-based games.', '2024-01-02', 'user2'),
('sd6', 'Battle Effects', 'Intense battle sounds.', '2024-01-03', 'user2');

-- Insert data into Scene
INSERT INTO ProjetInfo.Scene (id_scene, nom, description, date_creation)
VALUES
('scene1', 'Forest', 'Calm forest ambience.', '2024-01-04'),
('scene2', 'Dungeon', 'Echoing dungeon sounds.', '2024-01-05'),
('scene3', 'Spaceship Interior', 'Mechanical hums and alarms.', '2024-01-06'),
('scene4', 'Alien Planet', 'Strange and eerie sounds.', '2024-01-07'),
('scene5', 'Haunted House', 'Creepy old house sounds.', '2024-01-08'),
('scene6', 'Abandoned Hospital', 'Echoing halls and creepy whispers.', '2024-01-09'),
('scene7', 'Jungle', 'Sounds of exotic animals and trees.', '2024-01-10'),
('scene8', 'Beach', 'Waves crashing and seagulls.', '2024-01-11'),
('scene9', 'City Street', 'Cars honking and people chatting.', '2024-01-12'),
('scene10', 'Market Square', 'Busy market sounds.', '2024-01-13'),
('scene11', 'Battlefield', 'Explosions and war cries.', '2024-01-14'),
('scene12', 'Castle Siege', 'Sounds of a medieval battle.', '2024-01-15');

-- Insert data into Son
INSERT INTO ProjetInfo.Son (id_son, id_freesound, nom, description, duree)
VALUES
-- Random sounds
('son1', 'fs1', 'Rain', 'Light rain with occasional thunder.', '00:02:00'),
('son2', 'fs2', 'Wind Howling', 'Strong wind in the mountains.', '00:01:00'),
-- Continuous sounds
('son3', 'fs3', 'Birds Chirping', 'Soothing bird sounds.', '00:01:30'),
('son4', 'fs4', 'Ocean Waves', 'Gentle waves on the shore.', '00:03:00'),
-- Manual sounds
('son5', 'fs5', 'Sword Clash', 'Sound of swords clashing.', '00:00:05'),
('son6', 'fs6', 'Gunshot', 'Loud and sharp gunshot.', '00:00:02');

-- Add more sounds for variety
INSERT INTO ProjetInfo.Son (id_son, id_freesound, nom, description, duree)
VALUES
-- Random sounds
('son7', 'fs7', 'Thunder', 'Deep, rumbling thunder.', '00:01:00'),
('son8', 'fs8', 'Footsteps', 'Walking on dry leaves.', '00:00:45'),
-- Continuous sounds
('son9', 'fs9', 'Waterfall', 'Continuous sound of a waterfall.', '00:02:30'),
('son10', 'fs10', 'Crickets', 'Night-time cricket sounds.', '00:01:30'),
-- Manual sounds
('son11', 'fs11', 'Explosion', 'A large explosion sound.', '00:00:03'),
('son12', 'fs12', 'Door Creaking', 'Old wooden door creaking open.', '00:00:05');

-- Insert data into Tag
INSERT INTO ProjetInfo.Tag (nom_tag)
VALUES
('Relaxing'),
('Intense'),
('Ambient'),
('Natural'),
('Cinematic'),
('Eerie');

-- Associate Users with Sounddecks (User_Sounddeck)
INSERT INTO ProjetInfo.User_Sounddeck (id_user, id_sd)
VALUES
-- User 1's Sounddecks
('IUSZEM', 'sd1'),
('IUSZEM', 'sd2'),
('IUSZEM', 'sd3'),
-- User 2's Sounddecks
('user2', 'sd4'),
('user2', 'sd5'),
('user2', 'sd6');

-- Associate Sounddecks with Scenes (Sounddeck_Scene)
INSERT INTO ProjetInfo.Sounddeck_Scene (id_scene, id_sd)
VALUES
('scene1', 'sd1'), ('scene2', 'sd1'),
('scene3', 'sd2'), ('scene4', 'sd2'),
('scene5', 'sd3'), ('scene6', 'sd3'),
('scene7', 'sd4'), ('scene8', 'sd4'),
('scene9', 'sd5'), ('scene10', 'sd5'),
('scene11', 'sd6'), ('scene12', 'sd6');

-- Associate Scenes with Sons (Scene_Son)
INSERT INTO ProjetInfo.Scene_Son (id_scene, id_son, param1, param2, type)
VALUES
-- Forest Scene
('scene1', 'son1', '1', '2', 'aleatoire'),
('scene1', 'son2', '4', '20', 'aleatoire'),
('scene1', 'son3', 'none', 'none', 'continu'),
('scene1', 'son4', 'none', 'none', 'continu'),
('scene1', 'son5', 'a', 'none', 'manuel'),
('scene1', 'son6', 'b', 'none', 'manuel'),

-- Dungeon Scene
('scene2', 'son7', '20', '69', 'aleatoire'),
('scene2', 'son8', '4', '7', 'aleatoire'),
('scene2', 'son9', 'none', 'none', 'continu'),
('scene2', 'son10', 'none', 'none', 'continu'),
('scene2', 'son11', 'c', 'none', 'manuel'),
('scene2', 'son12', 'd', 'none', 'manuel');

-- Add similar associations for all other scenes...

-- Associate Sons with Tags (Son_Tag)
INSERT INTO ProjetInfo.Son_Tag (id_son, nom_tag)
VALUES
('son1', 'Relaxing'),
('son2', 'Ambient'),
('son3', 'Natural'),
('son4', 'Relaxing'),
('son5', 'Cinematic'),
('son6', 'Intense'),
('son7', 'Eerie'),
('son8', 'Natural'),
('son9', 'Natural'),
('son10', 'Relaxing'),
('son11', 'Intense'),
('son12', 'Eerie');
