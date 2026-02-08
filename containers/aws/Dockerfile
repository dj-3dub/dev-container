FROM alpine:latest

# Install AWS CLI v2 and SRE essentials via apk
RUN apk add --no-cache     aws-cli     curl     jq     groff     less

WORKDIR /aws

ENTRYPOINT ["aws"]
