import PropTypes from 'prop-types'

export const Header = (props) => {
  return (
    <>
        <h1>Hello from my react component</h1>
        <p>This is my props: {props.title}</p>
    </>
    )
}

Header.defaultProps = {
    title : 'Default title',
}

Header.propTypes = {
    title: PropTypes.string,
}