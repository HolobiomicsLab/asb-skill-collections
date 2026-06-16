# Evaluation Strategy

## Direct Checks

- verify HTTP GET request to https://metabologenomic.cbd.cs.cmu.edu/ returns status code 200 or other 2xx success code
- verify response contains valid HTML or JSON (file_format_is text/html or application/json)
- verify response body is non-empty (contains_substring of service identifier or title)
- verify DNS resolution succeeds for metabologenomic.cbd.cs.cmu.edu
- verify TLS/SSL certificate is valid and not expired

## Expert Review

- confirm that the returned page or API response is consistent with a deployed molDiscovery academic web service as described in the repository
- assess whether the service interface matches the deployment documentation referenced in the GitHub repository README
