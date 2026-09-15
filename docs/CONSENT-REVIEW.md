# Asking Luis Matos Azócar and Jean-Christophe Loubier to approve their entries

## How the page is closed

- The Frame Bureau page carries all six teachers, as written.
- `server.py` asks for a username and password on `/frame-bureau.html` only,
  whenever the `BUREAU_USERS` environment variable is set. Every other page,
  and the contact form, stays public and unchanged.
- While it is closed the page is served `noindex, nofollow, noarchive` and
  `no-store`, so it is not indexed or cached.
- `BUREAU_USERS` is formatted `name:password,name:password`, one login per
  reviewer, so the access log shows who opened it. Unset means the page is
  public, which is how the site normally runs.

## To set it up

1. In Render, on the service serving echoframe.co, add the environment variable
   `BUREAU_USERS` = `luis:<password-1>,jc:<password-2>`.
2. Send each person their own login with the note below.
3. When both have agreed, delete `BUREAU_USERS`. The page is public again with
   no other change. If one of them declines, remove their entry from `BENCH` in
   `scripts/frame_bureau.py` before reopening the page.

## The note to send

### Spanish — for Luis Matos Azócar

Asunto: Su perfil en la web de EchoFrame — ¿me confirma antes de publicarlo?

Estimado Luis:

Le escribo sobre The Frame Bureau, la división de formación de EchoFrame. Es la
versión renovada del OSINT Collective del que hablamos, reorganizada en cinco
módulos, y la estamos preparando como propuesta para el Qatar Leadership Center
de Doha, con quienes ya estamos en conversaciones. Tengo una reunión con ellos
el próximo lunes 21 de septiembre.

En la sección «Quién enseña» he escrito un párrafo sobre usted: su nombre, el
cargo de Chief Intelligence Architect y una breve descripción de su trayectoria.

La página está cerrada con contraseña mientras la revisan ustedes: no aparece en
los buscadores y solo se abre con estas credenciales:

  Enlace:      https://www.echoframe.co/frame-bureau-full.html
  Usuario:     luis
  Contraseña:  <password-1>

Le agradecería que leyera el párrafo que lleva su nombre y me dijera una de estas
tres cosas: que está de acuerdo tal como está, que quiere cambiar algo (dígame
qué y lo corrijo), o que prefiere no aparecer, en cuyo caso lo retiro sin más.

Nada se publica hasta que usted responda. Si pudiera decírmelo antes del lunes,
sabría con qué contar al presentarlo en Doha.

Un abrazo,
Robert

### French — for Jean-Christophe Loubier

Objet : Votre présentation sur le site EchoFrame — votre accord avant publication

Cher Jean-Christophe,

Je vous écris au sujet de The Frame Bureau, la division formation d'EchoFrame.
C'est la version repensée de l'OSINT Collective dont nous avions parlé,
réorganisée en cinq modules, et nous la préparons comme proposition pour le
Qatar Leadership Center de Doha, avec lequel nous sommes déjà en discussion.
J'ai un entretien avec eux lundi prochain, le 21 septembre.

Dans la rubrique « Qui enseigne », j'ai rédigé un paragraphe vous concernant :
votre nom, la fonction de Director of Decision Analytics et une courte
présentation de votre parcours.

La page est protégée par mot de passe le temps de votre relecture : elle
n'apparaît pas dans les moteurs de recherche et ne s'ouvre qu'avec les
identifiants ci-dessous.

  Lien :         https://www.echoframe.co/frame-bureau-full.html
  Identifiant :  jc
  Mot de passe : <password-2>

Pourriez-vous lire le paragraphe qui porte votre nom et me dire l'une de ces
trois choses : que vous l'approuvez tel quel, que vous souhaitez le modifier
(dites-moi quoi et je le corrige), ou que vous préférez ne pas y figurer, auquel
cas je le retire sans difficulté.

Rien ne sera publié avant votre réponse. Si vous pouviez me répondre avant lundi,
je saurais sur quoi compter au moment de le présenter à Doha.

Bien cordialement,
Robert
