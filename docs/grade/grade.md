# Grade

<script src="../_static/custom.js"></script>

<div id="description" style="border: 1px solid #ccc; padding: 10px; margin-top: 20px;">
  Click a requirement below to see details.
</div>

```{mermaid}
---
config: {"themeVariables": {"fontSize": "40px"}}
---
    flowchart TD
    subgraph Tier1 [Grades 3-]
        subgraph T1 [" "]
            direction TB
            uv@{ form: rounded, img: "../_static/img/logo/uv.svg", w: 200, h: 200}
            code@{ form: rounded, img: "../_static/img/logo/code.svg", w: 200, h: 200}
            pytest@{ img: "../_static/img/logo/pytest.svg", w: 200, h: 200}
            ruff@{ img: "../_static/img/logo/ruff.svg", w: 200, h: 200}
            
            uv --> code
            uv --> pytest
            uv --> ruff
        end
        style T1 fill:none,stroke:none
    end
     
    subgraph Tier2 [Grades 4-7]
        subgraph T2 [" "]
    
            direction LR
            subgraph T2L [" "]
                direction TB
                ty@{ img: "../_static/img/logo/ty.svg", w: 200, h: 200}
                readme@{ img: "../_static/img/logo/readme.svg", w: 200, h: 200}
                sphinx@{ img: "../_static/img/logo/sphinx.svg", w: 200, h: 200}
                sphinx_plus@{ img: "../_static/img/logo/sphinx_plus.svg", w: 200, h: 200}
                
                ty & readme --> sphinx --> sphinx_plus
            end
            subgraph T2R [" "]
                direction TB
                pytest_plus@{ img: "../_static/img/logo/pytest_plus.svg", w: 200, h: 200}
                cli@{ img: "../_static/img/logo/click.svg", w: 200, h: 200}
                poe@{ img: "../_static/img/logo/poe.svg", w: 200, h: 200}
                flamegraph@{ img: "../_static/img/logo/flamegraph.svg", w: 200, h: 200}
                
                pytest_plus & cli ~~~ poe & flamegraph
            end
           
            T2L ~~~ T2R
            
            style T2L fill:none,stroke:none,padding:200px
            style T2R fill:none,stroke:none,padding:200px
        end
        style T2 fill:none,stroke:none
    end
     
    subgraph Tier3 [Grades 8+]
        subgraph T3 [" "]
            direction TB
            sphinx_flamegraph@{ img: "../_static/img/logo/sphinx_flamegraph.svg", w: 200, h: 200}
            cicd@{ img: "../_static/img/logo/cicd.svg", w: 200, h: 200}
            pypi@{ img: "../_static/img/logo/pypi.svg", w: 200, h: 200}
        end
        style T3 fill:none,stroke:none
    end

    Tier1 ~~~ Tier2
    Tier2 ~~~ Tier3
    
    style Tier1 fill:none,stroke:#8ac76b,stroke-width:10
    style Tier2 fill:none,stroke:#8ac76b,stroke-width:10
    style Tier3 fill:none,stroke:#8ac76b,stroke-width:10

    click uv call showDescription(uv.html)
    click code call showDescription(code.html)
    click pytest call showDescription(pytest.html)
    click ruff call showDescription(ruff.html)
    
    click ty call showDescription(ty.html)
    click readme call showDescription(readme.html)
    click sphinx call showDescription(sphinx.html)
    click sphinx_plus call showDescription(sphinx_plus.html)
    click pytest_plus call showDescription(pytest_plus.html)
    click cli call showDescription(cli.html)
    click poe call showDescription(poe.html)
    click flamegraph call showDescription(flamegraph.html)
    
    click cicd call showDescription(cicd.html)
    click pypi call showDescription(pypi.html)
    click sphinx_flamegraph call showDescription(sphinx_flamegraph.html)
```
