#!/usr/bin/env python
"""Tests for refinableobj module."""

import unittest

import numpy

import diffpy.srfit.equation.literals as literals


class TestArgument(unittest.TestCase):

    def testInit(self):
        """Test that everthing initializes as expected."""
        a = literals.Argument()
        self.assertEqual(None, a._value)
        self.assertTrue(False is a.const)
        self.assertTrue(None is a.name)
        return

    def testValue(self):
        """Test value setting."""

        a = literals.Argument()

        # Test error when there is no value
        self.assertRaises(ValueError, a.getValue)

        # Test setting value
        a.setValue(3.14)
        self.assertAlmostEqual(a._value, 3.14)

        a.setValue(3.14)
        self.assertAlmostEqual(a.value, 3.14)
        return

class TestOperator(unittest.TestCase):

    def testInit(self):
        """Test that everthing initializes as expected."""
        op = literals.Operator(symbol = "+", operation = numpy.add, nin = 2)

        self.assertEqual("+", op.symbol)
        self.assertEqual(numpy.add, op.operation)
        self.assertEqual(2, op.nin)
        self.assertEqual(1, op.nout)
        self.assertEqual(None, op._value)
        self.assertEqual([], op.args)
        return

    def testValue(self):
        """Test value."""
        # Test addition and operations
        op = literals.Operator(symbol = "+", operation = numpy.add, nin = 2)
        a = literals.Argument(value = 0)
        b = literals.Argument(value = 0)

        op.addLiteral(a)
        op.addLiteral(b)

        self.assertAlmostEquals(0, op.value)

        # Test update from the nodes
        a.setValue(4)
        self.assertTrue(op._value is None)
        self.assertAlmostEqual(4, op.value)

        b.value = 2
        self.assertTrue(op._value is None)
        self.assertAlmostEqual(6, op.value)

        return

    def testAddLiteral(self):
        """Test adding a literal to an operator node."""
        op = literals.Operator(name = "add", symbol = "+", operation =
                numpy.add, nin = 2, nout = 1)

        self.assertRaises(ValueError, op.getValue)
        op._value = 1
        self.assertEqual(op.getValue(), 1)

        # Test addition and operations
        a = literals.Argument(name = "a", value = 0)
        b = literals.Argument(name = "b", value = 0)

        op.addLiteral(a)
        self.assertRaises(ValueError, op.getValue)

        op.addLiteral(b)
        self.assertAlmostEqual(op.getValue(), 0)

        a.setValue(1)
        b.setValue(2)
        self.assertAlmostEqual(op.getValue(), 3)

        a.setValue(None)
        self.assertRaises(ValueError, op.getValue)

        # Test for self-references

        # Try to add self
        op = literals.Operator(name = "add", symbol = "+", operation =
                numpy.add, nin = 2, nout = 1)
        op.addLiteral(a)
        self.assertRaises(ValueError, op.addLiteral, op)

        # Try to add argument that contains self
        op2 = literals.Operator(name = "sub", symbol = "-", operation =
                numpy.subtract, nin = 2, nout = 1)
        op2.addLiteral(op)
        self.assertRaises(ValueError, op.addLiteral, op2)

        return

class TestConvolutionOperator(unittest.TestCase):

    def testValue(self):
        """Make sure the convolution operator is working properly."""

        import numpy
        pi = numpy.pi
        exp = numpy.exp

        x = numpy.linspace(0, 10, 1000)

        mu1 = 4.5
        sig1 = 0.1
        mu2 = 2.5
        sig2 = 0.4

        g1 = exp(-0.5*((x-mu1)/sig1)**2)
        a1 = literals.Argument(name = "g1", value = g1)
        g2 = exp(-0.5*((x-mu2)/sig2)**2)
        a2 = literals.Argument(name = "g2", value = g2)

        op = literals.ConvolutionOperator()
        op.addLiteral(a1)
        op.addLiteral(a2)

        g3c = op.value

        mu3 = mu1
        sig3 = (sig1**2 + sig2**2)**0.5
        g3 = exp(-0.5*((x-mu3)/sig3)**2)
        g3 *= sum(g1)/sum(g3)

        self.assertAlmostEquals(sum(g3c), sum(g3))
        self.assertAlmostEquals(0, sum((g3-g3c)**2))
        return


if __name__ == "__main__":

    unittest.main()

