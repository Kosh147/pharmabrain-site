Good, the repository is already cloned. Before deploying the app under `/PharmAI/`, I'd first get the static website working on the root domain.

## 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

Start and enable:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

Check:

```bash
sudo systemctl status nginx
```

---

## 2. Move website to web root

Your repo is currently here:

```bash
/home/koshechkinkosta/pharmabrain.ru
```

Move it to `/var/www`:

```bash
sudo mkdir -p /var/www
sudo mv ~/pharmabrain.ru /var/www/pharmabrain.ru
```

Set permissions:

```bash
sudo chown -R www-data:www-data /var/www/pharmabrain.ru
sudo chmod -R 755 /var/www/pharmabrain.ru
```

Verify:

```bash
ls -la /var/www/pharmabrain.ru
```

You should see `index.html`.

---

## 3. Create Nginx site

Create:

```bash
sudo nano /etc/nginx/sites-available/pharmai
```

Put:

```nginx
server {
    listen 80;
    server_name pharmabrain.ru www.pharmabrain.ru;

    root /var/www/pharmabrain.ru;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/pharmai /etc/nginx/sites-enabled/
```

Remove default site:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Test config:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

---

## 4. Open firewall

If UFW is enabled:

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

---

## 5. Point DNS

Make sure:

```text
A  pharmabrain.ru      -> 158.160.179.86
A  www.pharmabrain.ru  -> 158.160.179.86
```

From your Mac:

```bash
dig pharmabrain.ru
```

or

```bash
nslookup pharmabrain.ru
```

The IP must be:

```text
158.160.179.86
```

---

## 6. Test HTTP

Once DNS propagates:

```bash
curl http://pharmabrain.ru
```

or open:

```text
http://pharmabrain.ru
```

You should see your landing page.

---

## 7. Add HTTPS

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Run:

```bash
sudo certbot --nginx -d pharmabrain.ru -d www.pharmabrain.ru
```

Choose:

```text
Redirect HTTP to HTTPS
```

Verify:

```bash
https://pharmabrain.ru
```

---

## 8. Final structure

After this stage:

```text
Nginx
 ├── /
 │    └── Static website
 │         (/var/www/pharmabrain.ru)
 │
 └── /PharmAI/
      └── FastAPI app (later)
           http://127.0.0.1:8002
```

Once the website is accessible at `https://pharmabrain.ru`, we can add the `/PharmAI/` reverse proxy and deploy your FastAPI service without breaking the website.
