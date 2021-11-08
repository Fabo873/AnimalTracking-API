INSERT INTO Age (name) VALUES
    ("Infancia"),
    ("Juventud"),
    ("Adulto"),
    ("Vejez"),
    ("No Identificable");

INSERT INTO Destination (name) VALUES
    ("Centro Veterinario"),
    ("Cautiverio"),
    ("Libertad"),
    ("Eutanacia"),
    ("Muerte");

INSERT INTO Gender (name) VALUES
    ("Hembra"),
    ("Macho"),
    ("No Identificable");

INSERT INTO AnimalType (name) VALUES
    ("Mamifero"),
    ("Reptil"),
    ("Ave"),
    ("Amfibio"),
    ("Insecto");

INSERT INTO Species (name) VALUES
    ("Panthera Onca"),
    ("Panthera Leo"),
    ("Panthera Pardus"),
    ("Panthera Tigris"),
    ("Panthera Uncia"),
    ("Neofelis");

INSERT INTO User (id, username, password) VALUES
    (1, "EduardoMendez", "gAAAAABhiIBTfrh1NXxZmCY1_DJdgNnsDdy5S40FZW5ixWEHISGoOaqZck8y5UoCIsE-BD3KZ1rNDc98kmfVtCDOqMm95MovuA=="),
    (2, "LuisGarcia", "gAAAAABhiIBTfrh1NXxZmCY1_DJdgNnsDdy5S40FZW5ixWEHISGoOaqZck8y5UoCIsE-BD3KZ1rNDc98kmfVtCDOqMm95MovuA=="),
    (3, "AndresAguirre", "gAAAAABhiIBTfrh1NXxZmCY1_DJdgNnsDdy5S40FZW5ixWEHISGoOaqZck8y5UoCIsE-BD3KZ1rNDc98kmfVtCDOqMm95MovuA==");

INSERT INTO Person (user_id, name, first_lastname, second_lastname) VALUES
    (1, "Eduardo", "Mendez", "Santa Ana"),
    (2, "Luis", "Garcia", "Miramontes"),
    (3, "Andres", "Aguirre", "Alvarez");