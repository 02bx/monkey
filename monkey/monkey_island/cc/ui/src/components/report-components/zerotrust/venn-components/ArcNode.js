import React from 'react'
import PropTypes from 'prop-types';
import * as d3 from 'd3'

class ArcNode extends React.Component {
  render() {
    let {prefix, index, data} = this.props;

    let arc = d3.arc().innerRadius(data.inner).outerRadius(data.outer).startAngle(0).endAngle(Math.PI * 2.0);
    let id = prefix + 'Node_' + index;

    return (
      <g transform={'rotate(180)'} id={data.node.pillar}>
        <path

          id={prefix + 'Node_' + index}
          className={'arcNode'}
          data-tooltip={data.tooltip}
          d={arc()}
          fill={data.hex}

        />
        <text x={0} dy={data.fontStyle.size * 1.2} fontSize={data.fontStyle.size} textAnchor='middle'
              pointerEvents={'none'}>
          <textPath href={'#' + id} startOffset={'26.4%'}>
            {data.label}
          </textPath>
        </text>
      </g>
    );
  }
}

ArcNode.propTypes = {
  data: PropTypes.object
};

export default ArcNode;
