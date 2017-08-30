class CW extends React.Component {
  render() {
    let wh = document.body.clientHeight - 100;
    return (
      <div>
        <header></header>
        <div style={{color: '#888'}}>{this.props.children}</div>
        <footer></footer>
      </div>
    );
  }
}
class VTag extends React.Component {
  render() {
    return (
      <div>好啊</div>
    );
  }
}
ReactDOM.render(
  <CW>
    <VTag />
  </CW>,
  document.getElementById('root')
);