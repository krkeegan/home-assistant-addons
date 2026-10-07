ARG BUILD_FROM
FROM ${BUILD_FROM}

ARG BUILD_ARCH
ARG GRAFANA_IMAGE_RENDERER_VERSION

RUN set -eux; \
		case "${BUILD_ARCH}" in \
			amd64) renderer_arch="linux-amd64" ;; \
			aarch64) renderer_arch="linux-arm64" ;; \
			*) echo "Unsupported arch: ${BUILD_ARCH}" >&2; exit 1 ;; \
		esac; \
		apk add --no-cache \
			ca-certificates \
			chromium \
			curl \
			freetype \
			harfbuzz \
			nss \
			ttf-freefont; \
		curl -fsSL -o /usr/local/bin/grafana-image-renderer \
			"https://github.com/grafana/grafana-image-renderer/releases/download/v${GRAFANA_IMAGE_RENDERER_VERSION}/grafana-image-renderer-${renderer_arch}"; \
		chmod +x /usr/local/bin/grafana-image-renderer

WORKDIR /data

COPY rootfs /

EXPOSE 8081
