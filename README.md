type this into terminal

```
URL=$(echo 'aHR0cHM6Ly9wcm8tdG8tY29sLmdpdGh1Yi5pby9kcmFnb25zLWV5ZS95b3VfYXJlX2luLmh0bQ==' | base64 -d); echo $URL; xdg-open $URL 2>/dev/null
```
