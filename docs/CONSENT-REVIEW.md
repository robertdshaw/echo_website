# Asking Luis Matos Azócar and Jean-Christophe Loubier to approve their entries

## Where their names appear on the site

1. **The Frame Bureau, "Who teaches it"** — a name, a role and a paragraph each.
   Withheld from the published page until each of them agrees. See
   `AWAITING_CONSENT` in `scripts/build.py`.
2. **About, "Expert perspectives"** — an attributed quotation from each of them.
   Still published. Decide separately whether these were given for publication.

## How the review copy works

- `scripts/build.py` writes the full page, both names included, to `review/frame-bureau.html`.
  That directory is never copied into `public/`, is git-ignored, and is rebuilt on every deploy.
- `server.py` serves it at `/review/frame-bureau.html` behind HTTP Basic auth,
  with `X-Robots-Tag: noindex, nofollow, noarchive` and `Cache-Control: no-store`.
- Credentials come from the `REVIEW_USERS` environment variable, formatted
  `name:password,name:password`. If it is unset the review area returns 503,
  so a misconfiguration closes the door rather than opening it.
- Each reviewer gets their own username, so the access log shows who opened it.

## To set it up

1. In Render, on the service serving echoframe.co, add an environment variable:
   `REVIEW_USERS` = `luis:<password-1>,jc:<password-2>`
2. Send each person their own username and password with the note below.
3. When someone approves, remove their name from `AWAITING_CONSENT` in
   `scripts/build.py` and push. Their card returns to the published page.
4. When both have answered, delete the `REVIEW_USERS` variable to close the area.

## The note to send

### Spanish — for Luis Matos Azócar

Asunto: Su perfil en la web de EchoFrame — ¿me confirma antes de publicarlo?

Estimado Luis:

Estamos preparando la página de The Frame Bureau, la división de formación de
EchoFrame, y en la sección «Quién enseña» he escrito un párrafo sobre usted: su
nombre, el cargo de Chief Intelligence Architect y una breve descripción de su
trayectoria.

No lo he publicado. La página está en un borrador privado, no aparece en el sitio
ni en los buscadores, y solo se abre con la contraseña que le envío aquí:

  Enlace:      https://www.echoframe.co/review/frame-bureau.html
  Usuario:     luis
  Contraseña:  <password-1>

Le agradecería que leyera el párrafo que lleva su nombre y me dijera una de estas
tres cosas: que está de acuerdo tal como está, que quiere cambiar algo (dígame
qué y lo corrijo), o que prefiere no aparecer, en cuyo caso lo retiro sin más.

Nada se publica hasta que usted responda.

Un abrazo,
Robert

### French — for Jean-Christophe Loubier

Objet : Votre présentation sur le site EchoFrame — votre accord avant publication

Cher Jean-Christophe,

Nous préparons la page de The Frame Bureau, la division formation d'EchoFrame.
Dans la rubrique « Qui enseigne », j'ai rédigé un paragraphe vous concernant :
votre nom, la fonction de Director of Decision Analytics et une courte
présentation de votre parcours.

Je ne l'ai pas publié. La page est un brouillon privé : elle n'apparaît ni sur le
site ni dans les moteurs de recherche, et ne s'ouvre qu'avec le mot de passe
ci-dessous.

  Lien :         https://www.echoframe.co/review/frame-bureau.html
  Identifiant :  jc
  Mot de passe : <password-2>

Pourriez-vous lire le paragraphe qui porte votre nom et me dire l'une de ces
trois choses : que vous l'approuvez tel quel, que vous souhaitez le modifier
(dites-moi quoi et je le corrige), ou que vous préférez ne pas y figurer, auquel
cas je le retire sans difficulté.

Rien ne sera publié avant votre réponse.

Bien cordialement,
Robert
