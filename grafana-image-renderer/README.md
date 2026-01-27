# Grafana Image Renderer Addon

This addon runs the Grafana Image Renderer service for rendering Grafana panels and dashboards as images.  This works in
conjunction with the [Grafana addon](https://github.com/hassio-addons/addon-grafana). That addon claims to have the
image renderer included as a plugin, but I have never been able to get it to work.  Plus installing the image render as
a plugin has been deprecated by Grafana for a while. Grafana recommends running the image-render as a separate docker instance.

## Configuration

Generally, there is no need to set anything here. This addon works fine out of the box.

- `log_level`: Logging level (trace, debug, info, warn, error).
- `rendering_mode`: Renderer mode (default, clustered).
- `chrome_args`: Extra Chromium arguments (optional).

## Grafana Addon Configuration

To get Grafana to render images using the renderer you need to include at least these env-vars in the Grafana plugin:
```yaml
env_vars:
  - name: GF_RENDERING_SERVER_URL
    value: http://e92f333d-grafana-image-renderer:8081/render
  - name: GF_RENDERING_CALLBACK_URL
    value: http://a0d7b954-grafana:3000/
```

Once you add these vars, restart Grafana.

## Create a Bearer Token

You then need to create a Bearer token inside Grafana.

1. Go to Administration → Service accounts.
2. Click Create service account.
3. Give it a name (e.g. HomeAssistant).
4. Set the Role to Viewer (Viewer is sufficient for rendering dashboards/panels).
5. Click Create.
6. Open the service account you just created.
7. Click Add token.
8. Set an optional expiration (or none).
9. Click Generate token.
10. Copy the token immediately — you won’t be able to see it again.

You likely want to save this in your `secrets.yaml` file.

## To Generate an Image

You can look up the various url arguments [here](https://deepwiki.com/grafana/grafana-image-renderer/5-api-reference).

In short here is an example:
```bash
curl -H "Authorization: Bearer <GRAFANA_TOKEN>" \
-o /config/www/grafana/panel.png \
"http://a0d7b954-grafana:3000/render/d-solo/anotreal7/DashBoardName?orgId=1&from=1737934249609&to=1769470249609&timezone=browser&panelId=2&width=450&height=200"
```
You can call this curl command from a shell script in Home Assistant to generate an image as you see fit. The image above would be visible at https://<homeassistant>/local/panel.png. See [http](https://www.home-assistant.io/integrations/http/#hosting-files)

You can get all the information you need by using the share -> embed tool in the UI to construct your urls.

### Render a single panel (most common)

**Path**

`/render/d-solo/<dashboard_uid>/<dashboard_slug>`

**Example**

`http://a0d7b954-grafana:3000/render/d-solo/anotreal7/DashBoardName?orgId=1&from=1737934249609&to=1769470249609&timezone=browser&panelId=2&width=450&height=200`

**Required parameters**

| Parameter | Notes |
| --- | --- |
| `panelId` | Must be numeric (e.g. 2, not panel-2) |
| `width` | Image width in pixels |
| `height` | Image height in pixels |

**Common optional parameters**

| Parameter | Description |
| --- | --- |
| `from` / `to` | Epoch ms or relative (now-24h) |
| `tz` | IANA timezone (avoid `browser`) |
| `theme` | `light` or `dark` |
| `scale` | DPI multiplier (e.g. 2) |
| `orgId` | Required in multi-org setups |

### Render an entire dashboard

**Path**

`/render/dashboard-solo/db/<dashboard_name>`

**Example**

`http://a0d7b954-grafana:3000/render/dashboard-solo/db/DashBoardName?orgId=1&from=now-6h&to=now&width=1000&height=500`